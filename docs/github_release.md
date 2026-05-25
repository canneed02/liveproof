# GitHub Release Draft

## Tag

```text
v0.1.0-rc1-frontier-v2
```

## Title

```text
LiveProof v0.1.0: RC v1 + Frontier v2
```

## Body

LiveProof is a verifier-backed post-training evaluation protocol for frontier
AI systems.

This release includes:

- eight deterministic task families
- RC v1 easy/medium/hard corpora
- Frontier v2 extreme corpus
- public/private corpus split
- deterministic local verifiers
- model evaluation through OpenAI-compatible APIs
- raw JSONL result files and Markdown reports

Measured result:

```text
deepseek-v4-pro on Frontier v2 extreme: 12/80 accepted, 15%, 0 API errors
```

Corpus hashes:

```text
RC v1 easy      6d2ada024c4af2874fda6ff8b2594e07607957c07e088559f528dd2a1ea68296
RC v1 medium    1260f19e5fced4714478081df4558077b52a4e73b6b56e4e05caa202d5bc315a
RC v1 hard      fd9f739df08684894274dc84c23f1e12dc27c30750b9ff2bdd39aed822e6b252
Frontier v2     024fd02a3ebc131519a663fd93941a201240698e3b26ec92c3633f28fa67a9c0
```

Supplement checksum:

```text
004383d73f22b6f0fca4659a2c77833b3db43679e87d17f1885bbe47bbec10e5
```

Primary verification:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
python3 -m unittest discover -s tests
liveproof audit --tasks corpus/v2_extreme_private.jsonl
```
