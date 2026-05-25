from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from .config import Settings
from .deepseek import DeepSeekClient
from .io import read_jsonl, read_tasks
from .model_selection import select_models
from .nvidia import NvidiaClient
from .schema import Task
from .verifier import verify


def completed_pairs(path: Path) -> set[tuple[str, str]]:
    if not path.exists():
        return set()
    pairs = set()
    for record in read_jsonl(path):
        if "model" in record and "id" in record:
            pairs.add((record["model"], record["id"]))
    return pairs


def make_client(settings: Settings, provider: str, max_concurrency: int | None = None):
    if provider == "nvidia":
        return NvidiaClient(
            base_url=settings.base_url,
            api_keys=settings.api_keys,
            timeout_seconds=settings.timeout_seconds,
            max_concurrency=max_concurrency or settings.max_concurrency,
            retries=settings.retries,
            max_tokens=settings.max_tokens,
            system_prompt=settings.system_prompt,
        )
    if provider == "deepseek":
        return DeepSeekClient(
            base_url=settings.deepseek_base_url,
            api_key=settings.deepseek_api_key,
            timeout_seconds=settings.timeout_seconds,
            max_concurrency=max_concurrency or settings.max_concurrency,
            retries=settings.retries,
            max_tokens=settings.max_tokens,
            system_prompt=settings.system_prompt,
        )
    raise ValueError(f"Unknown provider: {provider}")


async def discover_models(settings: Settings, limit: int, provider: str = "nvidia") -> tuple[str, ...]:
    client = make_client(settings, provider, max_concurrency=1)
    try:
        available = await client.list_models()
    finally:
        await client.close()
    return tuple(choice.id for choice in select_models(available, limit=limit))


async def run_model_eval(
    *,
    settings: Settings,
    tasks_path: Path,
    out_path: Path,
    models: tuple[str, ...],
    provider: str = "nvidia",
    limit: int | None = None,
    resume: bool = True,
) -> int:
    tasks = read_tasks(tasks_path)
    if limit is not None:
        tasks = tasks[:limit]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = completed_pairs(out_path) if resume else set()
    queue = [
        (model, task)
        for model in models
        for task in tasks
        if (model, task.id) not in done
    ]
    if not queue:
        return 0

    client = make_client(settings, provider)
    write_lock = asyncio.Lock()
    written = 0
    try:
        async def worker(model: str, task: Task) -> None:
            nonlocal written
            record = await _evaluate_one(client, model, task)
            async with write_lock:
                with out_path.open("a") as handle:
                    handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
                written += 1
                print(f"{written}/{len(queue)}\t{model}\t{task.id}\t{record['status']}", flush=True)

        await asyncio.gather(*(worker(model, task) for model, task in queue))
    finally:
        await client.close()
    return written


async def _evaluate_one(client, model: str, task: Task) -> dict:
    started = datetime.now(timezone.utc)
    try:
        completion = await client.chat(model=model, prompt=_eval_prompt(task.prompt))
        ok, note = verify(task, completion.text)
        return {
            "ts": started.isoformat(),
            "id": task.id,
            "family": task.family,
            "profile": str(task.verifier.get("profile", "unknown")),
            "task_hash": task.public_record()["task_hash"],
            "prompt": task.prompt,
            "model": model,
            "provider": client.__class__.__name__.replace("Client", "").lower(),
            "status": "accepted" if ok else "rejected",
            "answer": completion.text.strip(),
            "verifier_note": note,
            "raw": completion.raw,
            "error": None,
        }
    except Exception as exc:
        return {
            "ts": started.isoformat(),
            "id": task.id,
            "family": task.family,
            "profile": str(task.verifier.get("profile", "unknown")),
            "task_hash": task.public_record()["task_hash"],
            "prompt": task.prompt,
            "model": model,
            "provider": client.__class__.__name__.replace("Client", "").lower(),
            "status": "error",
            "answer": "",
            "verifier_note": "api error",
            "raw": {},
            "error": str(exc),
        }


def _eval_prompt(prompt: str) -> str:
    return (
        f"{prompt}\n\n"
        "Important: return exactly one XML tag: <answer>...</answer>. "
        "Put the final answer inside the tag and nothing else."
    )
