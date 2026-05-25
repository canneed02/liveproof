from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .schema import Task


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def read_tasks(path: Path) -> list[Task]:
    tasks = []
    for record in read_jsonl(path):
        tasks.append(
            Task(
                id=record["id"],
                family=record["family"],
                seed=record["seed"],
                prompt=record["prompt"],
                verifier=record["verifier"],
                answer=record["answer"],
            )
        )
    return tasks

