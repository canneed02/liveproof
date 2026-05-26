# Research Foundry

Research Foundry is the autonomous LiveProof lab loop.

It runs on the server, generates fresh seed-based tasks, audits private
verifier payloads, evaluates NVIDIA-hosted models, writes a research ledger, and
pushes a review branch. It does not submit arXiv papers, post Hacker News
threads, publish final releases, or push directly to `main`.

## Safety Boundary

Allowed:

- generate fresh corpora
- run budget-limited NVIDIA evaluations
- write Markdown ledgers
- commit public prompts and result files
- push branches named `agent/...`

Not allowed:

- use DeepSeek credentials
- commit `.env`
- commit private corpora
- force-push or delete branches
- publish final releases without human approval
- submit arXiv or Hacker News posts

## Server Install

```bash
sudo install -m 0644 ops/research-foundry.service /etc/systemd/system/research-foundry.service
sudo install -m 0644 ops/research-foundry.timer /etc/systemd/system/research-foundry.timer
sudo systemctl daemon-reload
sudo systemctl enable --now research-foundry.timer
```

Manual one-shot run:

```bash
FOUNDRY_PUSH=1 scripts/research_foundry.py --repo /root/liveproof-agent --task-count 24 --eval-limit 8 --model-limit 3
```

## Human Gate

Review pushed `agent/...` branches before merging or publishing. A foundry
branch is evidence collection, not a scientific claim by itself.

## Governance

Governance hardening for the LiveProof-specific foundry is tracked in:

- `docs/governance.md`

Broader autonomous research planning now lives outside LiveProof in the
independent AxiomForge project.
