# LiveProof RC v1 + Frontier v2 Release Manifest

Release name:

```text
liveproof-rc-v1-frontier-v2
```

Core claim:

```text
Static benchmarks decay under adaptive optimization. Fresh seed-generated tasks
with deterministic verifiers expose structured algorithmic blind spots that a
single aggregate benchmark score can hide.
```

Included code:

- `src/liveproof/`
- `tests/`
- `scripts/reproduce_ladder.sh`
- `pyproject.toml`
- `README.md`
- `.gitignore`
- `LICENSE`
- `CITATION.cff`
- `ETHICS.md`
- `SECURITY.md`
- `CONTRIBUTING.md`

Included docs:

- `docs/technical_note.md`
- `docs/ladder_protocol.md`
- `docs/ladder_study.md`
- `docs/release_candidate.md`
- `docs/deepseek_v4_pro_study.md`
- `docs/frontier_v2.md`
- `docs/preprint.md`
- `docs/publication_plan.md`
- `docs/github_release.md`

Included RC v1 data:

- `corpus/rc_v1_easy_public.jsonl`
- `corpus/rc_v1_medium_public.jsonl`
- `corpus/rc_v1_hard_public.jsonl`
- `corpus/rc_v1_easy_private.jsonl`
- `corpus/rc_v1_medium_private.jsonl`
- `corpus/rc_v1_hard_private.jsonl`
- `corpus/rc_v1_study_8x2x3_20260525T063550Z.results.jsonl`
- `corpus/rc_v1_study_8x2x3_20260525T063550Z.md`
- `corpus/deepseek_v4_pro_rc_study_8x3_20260525T064933Z.results.jsonl`
- `corpus/deepseek_v4_pro_rc_study_8x3_20260525T064933Z.md`

Included Frontier v2 data:

- `corpus/v2_extreme_public.jsonl`
- `corpus/v2_extreme_private.jsonl`
- `corpus/deepseek_v4_pro_v2_extreme_80_20260525T191654Z.results.jsonl`
- `corpus/deepseek_v4_pro_v2_extreme_80_20260525T191654Z.md`
- `corpus/README.md`

RC v1 seed:

```text
2026-05-25-rc-v1
```

RC v1 corpus hashes:

```text
easy   6d2ada024c4af2874fda6ff8b2594e07607957c07e088559f528dd2a1ea68296
medium 1260f19e5fced4714478081df4558077b52a4e73b6b56e4e05caa202d5bc315a
hard   fd9f739df08684894274dc84c23f1e12dc27c30750b9ff2bdd39aed822e6b252
```

Frontier v2 seed:

```text
2026-05-25-frontier-v2
```

Frontier v2 corpus hash:

```text
extreme 024fd02a3ebc131519a663fd93941a201240698e3b26ec92c3633f28fa67a9c0
```

Frontier v2 initial model result:

```text
deepseek-v4-pro: 12/80 accepted on the full extreme corpus, 15%
```

Excluded:

- `.env`
- `.venv/`
- `__pycache__/`
- provider API keys
- exploratory non-RC corpus files
- temporary canary runs

Verification:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
python3 -m unittest discover -s tests
liveproof audit --tasks corpus/rc_v1_easy_private.jsonl
liveproof audit --tasks corpus/rc_v1_medium_private.jsonl
liveproof audit --tasks corpus/rc_v1_hard_private.jsonl
liveproof audit --tasks corpus/v2_extreme_private.jsonl
```
