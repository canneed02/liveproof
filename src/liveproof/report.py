from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


def generate_report(results_path: Path, out_path: Path) -> None:
    records = [json.loads(line) for line in results_path.read_text().splitlines() if line.strip()]
    if not records:
        raise ValueError(f"No records found in {results_path}")

    by_model: dict[str, list[dict]] = defaultdict(list)
    by_family: dict[tuple[str, str], list[dict]] = defaultdict(list)
    by_profile: dict[tuple[str, str], list[dict]] = defaultdict(list)
    by_profile_family: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for record in records:
        by_model[record["model"]].append(record)
        by_family[(record["model"], record["family"])].append(record)
        profile = record.get("profile", "unknown")
        by_profile[(record["model"], profile)].append(record)
        by_profile_family[(record["model"], profile, record["family"])].append(record)

    lines = [
        "# LiveProof Model Study",
        "",
        f"Results file: `{results_path}`",
        f"Records: {len(records)}",
        f"Models: {len(by_model)}",
        "",
        "## Model Leaderboard",
        "",
        "| Model | Accepted | Rejected | Errors | Total | Acceptance |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model, items in sorted(by_model.items()):
        accepted = sum(item["status"] == "accepted" for item in items)
        rejected = sum(item["status"] == "rejected" for item in items)
        errors = sum(item["status"] == "error" for item in items)
        total = len(items)
        lines.append(f"| `{model}` | {accepted} | {rejected} | {errors} | {total} | {accepted / total:.0%} |")

    lines.extend(["", "## Family Matrix", ""])
    lines.extend(["| Model | Family | Accepted | Total | Acceptance |", "| --- | --- | ---: | ---: | ---: |"])
    for (model, family), items in sorted(by_family.items()):
        accepted = sum(item["status"] == "accepted" for item in items)
        lines.append(f"| `{model}` | `{family}` | {accepted} | {len(items)} | {accepted / len(items):.0%} |")

    lines.extend(["", "## Difficulty Matrix", ""])
    lines.extend(["| Model | Profile | Accepted | Total | Acceptance |", "| --- | --- | ---: | ---: | ---: |"])
    for (model, profile), items in sorted(by_profile.items()):
        accepted = sum(item["status"] == "accepted" for item in items)
        lines.append(f"| `{model}` | `{profile}` | {accepted} | {len(items)} | {accepted / len(items):.0%} |")

    lines.extend(["", "## Difficulty x Family", ""])
    lines.extend(["| Model | Profile | Family | Accepted | Total | Acceptance |", "| --- | --- | --- | ---: | ---: | ---: |"])
    for (model, profile, family), items in sorted(by_profile_family.items()):
        accepted = sum(item["status"] == "accepted" for item in items)
        lines.append(f"| `{model}` | `{profile}` | `{family}` | {accepted} | {len(items)} | {accepted / len(items):.0%} |")

    failures = [item for item in records if item["status"] != "accepted"]
    lines.extend(["", "## Failures", ""])
    if not failures:
        lines.append("No failures.")
    else:
        for item in failures[:80]:
            lines.extend(
                [
                    f"### {item['model']} / {item['id']}",
                    "",
                    f"- Family: `{item['family']}`",
                    f"- Profile: `{item.get('profile', 'unknown')}`",
                    f"- Task hash: `{item.get('task_hash', 'unknown')}`",
                    f"- Status: `{item['status']}`",
                    f"- Verifier: {item['verifier_note']}",
                    f"- Error: {item.get('error') or 'none'}",
                    "",
                    "Prompt:",
                    "",
                    "```text",
                    item.get("prompt", "").strip(),
                    "```",
                    "",
                    "Answer:",
                    "",
                    "```text",
                    item.get("answer", "").strip(),
                    "```",
                    "",
                ]
            )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
