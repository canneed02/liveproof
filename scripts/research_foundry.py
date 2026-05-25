#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_REPO = Path("/root/liveproof-agent")
DEFAULT_DB = Path("/root/research-foundry/foundry.db")
DEFAULT_STATE_DIR = Path("/root/research-foundry")


@dataclass(frozen=True)
class FoundryConfig:
    repo: Path
    db: Path
    state_dir: Path
    task_count: int
    eval_limit: int
    model_limit: int
    max_concurrency: int
    push: bool
    remote: str


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one audited LiveProof research-foundry cycle.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE_DIR)
    parser.add_argument("--task-count", type=int, default=int(os.getenv("FOUNDRY_TASK_COUNT", "24")))
    parser.add_argument("--eval-limit", type=int, default=int(os.getenv("FOUNDRY_EVAL_LIMIT", "8")))
    parser.add_argument("--model-limit", type=int, default=int(os.getenv("FOUNDRY_MODEL_LIMIT", "3")))
    parser.add_argument("--max-concurrency", type=int, default=int(os.getenv("FOUNDRY_MAX_CONCURRENCY", "3")))
    parser.add_argument("--push", action="store_true", default=os.getenv("FOUNDRY_PUSH", "0") == "1")
    parser.add_argument("--remote", default=os.getenv("FOUNDRY_REMOTE", "origin"))
    args = parser.parse_args()

    config = FoundryConfig(
        repo=args.repo,
        db=args.db,
        state_dir=args.state_dir,
        task_count=args.task_count,
        eval_limit=args.eval_limit,
        model_limit=args.model_limit,
        max_concurrency=args.max_concurrency,
        push=args.push,
        remote=args.remote,
    )
    run_cycle(config)


def run_cycle(config: FoundryConfig) -> None:
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    day = now.strftime("%Y-%m-%d")
    seed = f"foundry-frontier-v3-{stamp}"
    branch = f"agent/foundry-{stamp}"
    run_id = f"foundry_{stamp}"

    config.state_dir.mkdir(parents=True, exist_ok=True)
    config.db.parent.mkdir(parents=True, exist_ok=True)
    init_db(config.db)

    private_tasks = config.state_dir / "private_corpus" / f"{run_id}_private.jsonl"
    public_tasks = config.repo / "corpus" / f"{run_id}_public.jsonl"
    results = config.repo / "corpus" / f"{run_id}_nvidia.results.jsonl"
    report = config.repo / "corpus" / f"{run_id}_nvidia.md"
    ledger = config.repo / "docs" / "research" / f"{day}-{run_id}.md"

    private_tasks.parent.mkdir(parents=True, exist_ok=True)
    public_tasks.parent.mkdir(parents=True, exist_ok=True)
    ledger.parent.mkdir(parents=True, exist_ok=True)

    started = datetime.now(timezone.utc)
    commands: list[str] = []
    status = "started"
    error = ""

    try:
        require_clean_or_agent_branch(config.repo)
        checkout_branch(config.repo, branch)

        run_liveproof(
            config,
            [
                "generate",
                "--seed",
                seed,
                "--profile",
                "extreme",
                "--count",
                str(config.task_count),
                "--out",
                str(private_tasks),
                "--public-out",
                str(public_tasks),
            ],
            commands,
        )
        audit_out = run_liveproof(config, ["audit", "--tasks", str(private_tasks)], commands)

        model_out = run_liveproof(
            config,
            ["models", "--provider", "nvidia", "--limit", str(config.model_limit)],
            commands,
        )
        models = parse_models(model_out, config.model_limit)
        if not models:
            raise RuntimeError("NVIDIA model discovery returned no models")

        env = os.environ.copy()
        env["LIVEPROOF_MAX_CONCURRENCY"] = str(config.max_concurrency)
        run_liveproof(
            config,
            [
                "eval",
                "--provider",
                "nvidia",
                "--models",
                ",".join(models),
                "--limit",
                str(config.eval_limit),
                "--tasks",
                str(private_tasks),
                "--out",
                str(results),
            ],
            commands,
            env=env,
            timeout=3600,
        )
        run_liveproof(config, ["report", "--results", str(results), "--out", str(report)], commands)

        summary = summarize_results(results)
        ledger.write_text(
            render_ledger(
                run_id=run_id,
                seed=seed,
                branch=branch,
                public_tasks=public_tasks,
                private_tasks=private_tasks,
                results=results,
                report=report,
                audit=audit_out,
                models=models,
                summary=summary,
                commands=commands,
            )
        )

        git_add_commit(config.repo, [public_tasks, results, report, ledger], f"Add foundry run {run_id}")
        if config.push:
            git(config.repo, ["push", "-u", config.remote, branch], timeout=600)
        status = "completed"
    except Exception as exc:
        status = "failed"
        error = str(exc)
        failure = config.state_dir / "failures" / f"{run_id}.txt"
        failure.parent.mkdir(parents=True, exist_ok=True)
        failure.write_text(f"{type(exc).__name__}: {exc}\n")
        raise
    finally:
        finished = datetime.now(timezone.utc)
        record_run(config.db, run_id, started, finished, status, seed, branch, error)


def init_db(path: Path) -> None:
    with sqlite3.connect(path) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                started TEXT NOT NULL,
                finished TEXT NOT NULL,
                status TEXT NOT NULL,
                seed TEXT NOT NULL,
                branch TEXT NOT NULL,
                error TEXT NOT NULL
            )
            """
        )


def record_run(
    path: Path,
    run_id: str,
    started: datetime,
    finished: datetime,
    status: str,
    seed: str,
    branch: str,
    error: str,
) -> None:
    with sqlite3.connect(path) as db:
        db.execute(
            """
            INSERT OR REPLACE INTO runs
            (run_id, started, finished, status, seed, branch, error)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (run_id, started.isoformat(), finished.isoformat(), status, seed, branch, error),
        )


def require_clean_or_agent_branch(repo: Path) -> None:
    branch = git(repo, ["branch", "--show-current"]).strip()
    dirty = git(repo, ["status", "--short"]).strip()
    if dirty and not branch.startswith("agent/"):
        raise RuntimeError(f"refusing to run on dirty non-agent branch {branch!r}")


def checkout_branch(repo: Path, branch: str) -> None:
    git(repo, ["fetch", "origin", "main"], timeout=300, check=False)
    git(repo, ["checkout", "-B", branch, "origin/main"])


def run_liveproof(
    config: FoundryConfig,
    args: list[str],
    commands: list[str],
    *,
    env: dict[str, str] | None = None,
    timeout: int = 900,
) -> str:
    cmd = [str(config.repo / ".venv" / "bin" / "liveproof"), *args]
    if not Path(cmd[0]).exists():
        cmd = ["liveproof", *args]
    commands.append(" ".join(cmd))
    proc = subprocess.run(
        cmd,
        cwd=config.repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        timeout=timeout,
        check=True,
    )
    return proc.stdout


def parse_models(output: str, limit: int) -> list[str]:
    models: list[str] = []
    for line in output.splitlines():
        if line.startswith("available=") or not line.strip():
            continue
        models.append(line.split("\t", 1)[0].strip())
    return models[:limit]


def summarize_results(path: Path) -> dict:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    by_model: dict[str, dict[str, int]] = {}
    by_family: dict[str, dict[str, int]] = {}
    for row in rows:
        model = row.get("model", "unknown")
        family = row.get("family", "unknown")
        status = row.get("status", "unknown")
        by_model.setdefault(model, {"accepted": 0, "rejected": 0, "error": 0, "total": 0})
        by_family.setdefault(family, {"accepted": 0, "rejected": 0, "error": 0, "total": 0})
        bucket = "error" if status == "error" else status
        if bucket not in {"accepted", "rejected", "error"}:
            bucket = "rejected"
        by_model[model][bucket] += 1
        by_model[model]["total"] += 1
        by_family[family][bucket] += 1
        by_family[family]["total"] += 1
    return {"records": len(rows), "by_model": by_model, "by_family": by_family}


def render_ledger(
    *,
    run_id: str,
    seed: str,
    branch: str,
    public_tasks: Path,
    private_tasks: Path,
    results: Path,
    report: Path,
    audit: str,
    models: list[str],
    summary: dict,
    commands: list[str],
) -> str:
    return f"""# Research Foundry Ledger: {run_id}

## Claim Under Test

Fresh Frontier v3-style extreme tasks should continue exposing family-specific
algorithmic blind spots under NVIDIA-hosted model evaluation.

## Seed

```text
{seed}
```

## Branch

```text
{branch}
```

## Model Set

```text
{", ".join(models)}
```

## Artifacts

- Public tasks: `{relative(public_tasks)}`
- Private tasks: `{private_tasks}`
- Results: `{relative(results)}`
- Report: `{relative(report)}`

Private tasks stay on the server and are not committed to the public branch.

## Audit

```text
{audit.strip()}
```

## Summary

```json
{json.dumps(summary, indent=2, sort_keys=True)}
```

## Skeptic Notes

- This is an autonomous scout run, not a final leaderboard.
- The task count and per-model limit are intentionally budget-constrained.
- Any public claim must be re-run with a frozen seed, full corpus, and clean
  release packaging.
- The branch is suitable for review; it is not a publication approval.

## Commands

```text
{chr(10).join(commands)}
```
"""


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(DEFAULT_REPO))
    except ValueError:
        return str(path)


def git_add_commit(repo: Path, paths: list[Path], message: str) -> None:
    rels = [str(path.relative_to(repo)) for path in paths]
    git(repo, ["add", "-f", *rels])
    if git(repo, ["diff", "--cached", "--quiet"], check=False).returncode == 0:
        return
    git(repo, ["commit", "-m", message])


def git(repo: Path, args: list[str], *, timeout: int = 120, check: bool = True):
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=check,
    ).stdout if check else subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )


if __name__ == "__main__":
    main()
