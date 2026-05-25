from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from .config import load_settings
from .evaluator import discover_models, run_model_eval
from .generators import generate_tasks
from .io import read_jsonl, read_tasks, write_jsonl
from .model_selection import select_models
from .nvidia import NvidiaClient
from .report import generate_report
from .schema import stable_hash
from .verifier import solve, verify


def main() -> None:
    parser = argparse.ArgumentParser(prog="liveproof")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser("generate", help="Generate verifier-backed tasks.")
    gen.add_argument("--seed", required=True)
    gen.add_argument("--count", type=int, required=True)
    gen.add_argument("--profile", choices=["easy", "medium", "hard", "extreme"], default="medium")
    gen.add_argument("--out", type=Path, required=True)
    gen.add_argument("--public-out", type=Path)

    solve_parser = subparsers.add_parser("solve", help="Write built-in solver answers.")
    solve_parser.add_argument("--tasks", type=Path, required=True)
    solve_parser.add_argument("--out", type=Path, required=True)

    verify_parser = subparsers.add_parser("verify", help="Verify submitted answers.")
    verify_parser.add_argument("--tasks", type=Path, required=True)
    verify_parser.add_argument("--answers", type=Path, required=True)

    audit = subparsers.add_parser("audit", help="Validate a private corpus.")
    audit.add_argument("--tasks", type=Path, required=True)

    models_parser = subparsers.add_parser("models", help="Discover and rank NVIDIA models.")
    models_parser.add_argument("--limit", type=int, default=6)
    models_parser.add_argument("--provider", choices=["nvidia", "deepseek"], default="nvidia")

    eval_parser = subparsers.add_parser("eval", help="Run model answers through LiveProof verifiers.")
    eval_parser.add_argument("--tasks", type=Path, required=True)
    eval_parser.add_argument("--out", type=Path, required=True)
    eval_parser.add_argument("--models", help="Comma-separated model ids. Use auto to discover.")
    eval_parser.add_argument("--provider", choices=["nvidia", "deepseek"], default="nvidia")
    eval_parser.add_argument("--model-limit", type=int, default=4)
    eval_parser.add_argument("--limit", type=int, help="Limit tasks per model.")
    eval_parser.add_argument("--no-resume", action="store_true")

    report_parser = subparsers.add_parser("report", help="Generate Markdown report from model results.")
    report_parser.add_argument("--results", type=Path, required=True)
    report_parser.add_argument("--out", type=Path, required=True)

    args = parser.parse_args()

    if args.command == "generate":
        tasks = generate_tasks(args.seed, args.count, profile=args.profile)
        write_jsonl(args.out, (task.private_record() for task in tasks))
        if args.public_out:
            write_jsonl(args.public_out, (task.public_record() for task in tasks))
        print(f"generated={len(tasks)} private={args.out}")
        if args.public_out:
            print(f"public={args.public_out}")
        print(f"manifest_hash={stable_hash([task.public_record() for task in tasks])}")
        return

    if args.command == "solve":
        tasks = read_tasks(args.tasks)
        write_jsonl(args.out, ({"id": task.id, "answer": solve(task)} for task in tasks))
        print(f"wrote={len(tasks)} answers={args.out}")
        return

    if args.command == "verify":
        tasks = {task.id: task for task in read_tasks(args.tasks)}
        answers = read_jsonl(args.answers)
        accepted = 0
        for answer in answers:
            task = tasks.get(answer["id"])
            if task is None:
                print(f"{answer['id']}\trejected\tunknown task")
                continue
            ok, note = verify(task, str(answer.get("answer", "")))
            accepted += int(ok)
            print(f"{answer['id']}\t{'accepted' if ok else 'rejected'}\t{note}")
        print(f"accepted={accepted} total={len(answers)}")
        raise SystemExit(0 if accepted == len(answers) else 1)

    if args.command == "audit":
        tasks = read_tasks(args.tasks)
        seen = set()
        for task in tasks:
            if task.id in seen:
                raise SystemExit(f"duplicate task id: {task.id}")
            seen.add(task.id)
            expected = solve(task)
            ok, note = verify(task, task.answer)
            if not ok:
                raise SystemExit(f"audit failed for {task.id}: {note}; solver={expected}")
        print(f"audit=ok tasks={len(tasks)} corpus_hash={stable_hash([task.public_record() for task in tasks])}")
        return

    if args.command == "models":
        settings = load_settings()

        async def _run() -> None:
            from .evaluator import make_client

            client = make_client(settings, args.provider, max_concurrency=1)
            try:
                available = await client.list_models()
            finally:
                await client.close()
            print(f"available={len(available)}")
            for choice in select_models(available, limit=args.limit):
                print(f"{choice.id}\t{choice.reason}")

        asyncio.run(_run())
        return

    if args.command == "eval":
        settings = load_settings()
        if args.models and args.models != "auto":
            models = tuple(item.strip() for item in args.models.split(",") if item.strip())
        else:
            models = asyncio.run(discover_models(settings, args.model_limit, provider=args.provider))
        print("models=" + ",".join(models), flush=True)
        written = asyncio.run(
            run_model_eval(
                settings=settings,
                tasks_path=args.tasks,
                out_path=args.out,
                models=models,
                provider=args.provider,
                limit=args.limit,
                resume=not args.no_resume,
            )
        )
        print(f"written={written} out={args.out}")
        return

    if args.command == "report":
        generate_report(args.results, args.out)
        print(f"report={args.out}")
        return

    raise SystemExit(f"unknown command: {args.command}")


if __name__ == "__main__":
    main()
