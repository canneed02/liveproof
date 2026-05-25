# Ethics and Responsible Use

LiveProof is an evaluation protocol. It is intended to measure model reliability
on fresh, verifier-backed algorithmic tasks without relying on model judges.

## Intended Uses

- post-training evaluation of AI systems
- reproducible research on benchmark contamination and benchmark saturation
- task-family analysis of reasoning failures
- comparison of model behavior under fixed scoring rules

## Non-Goals

LiveProof is not a safety jailbreak suite, exploit framework, or tool for
extracting private model information. The included task families are synthetic
algorithmic tasks with deterministic local verifiers.

## Publication Policy

Public corpora may be committed directly to a repository. Private corpora and
answer-bearing verifier payloads should be handled as frozen supplements when
the goal is reproducible science, and withheld from public leaderboards when the
goal is future blind evaluation.

## Reporting

Reports should clearly distinguish measured results from estimates. Aggregate
scores should be accompanied by family-level breakdowns because LiveProof is
designed to expose structured failure profiles, not only a single leaderboard
number.
