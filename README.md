# LiveProof

LiveProof is a verifier-backed evaluation protocol for frontier AI systems.

The core idea is simple: static benchmarks rot. If a benchmark is public,
finite, reused, and worth optimizing against, it eventually stops measuring
what people claim it measures. LiveProof replaces fixed questions with
post-training generated tasks whose answers are checked by deterministic
verifiers.

This repository contains:

- deterministic task generation from a public seed
- private verifier payloads and public prompts
- local solvers used only for audit and corpus validation
- answer verification without model judges
- a technical note with the core impossibility argument
- a publication-ready RC v1 + Frontier v2 artifact

No model API calls are required to use the generator or verifier.

## Primary Result

DeepSeek V4 Pro on the full Frontier v2 `extreme` corpus:

| Model | Accepted | Rejected | Errors | Total | Acceptance |
| --- | ---: | ---: | ---: | ---: | ---: |
| `deepseek-v4-pro` | 12 | 68 | 0 | 80 | 15% |

Family-level signal:

| Family | Accepted | Total | Acceptance |
| --- | ---: | ---: | ---: |
| `affine_mod` | 0 | 10 | 0% |
| `boolean_count` | 0 | 10 | 0% |
| `counterexample_search` | 1 | 10 | 10% |
| `dfa_shortest` | 1 | 10 | 10% |
| `graph_intervention` | 10 | 10 | 100% |
| `grid_checksum` | 0 | 10 | 0% |
| `program_trace` | 0 | 10 | 0% |
| `string_rewrite` | 0 | 10 | 0% |

The important result is the structured profile, not only the aggregate score:
the model solves graph reachability interventions but collapses on most
algorithmic state-tracking families.

## Quickstart

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .

liveproof generate --seed 2026-05-24-liveproof --profile medium --count 24 --out corpus/private.jsonl --public-out corpus/public.jsonl
liveproof solve --tasks corpus/private.jsonl --out corpus/private.answers.jsonl
liveproof verify --tasks corpus/private.jsonl --answers corpus/private.answers.jsonl
liveproof audit --tasks corpus/private.jsonl
```

To reproduce the local verifier pipeline across the difficulty ladder:

```bash
scripts/reproduce_ladder.sh 2026-05-25-ladder-v1 40
```

The frontier-grade `extreme` profile is also available:

```bash
liveproof generate --seed 2026-05-25-frontier-v2 --profile extreme --count 80 --out corpus/v2_extreme_private.jsonl --public-out corpus/v2_extreme_public.jsonl
liveproof audit --tasks corpus/v2_extreme_private.jsonl
```

## Task Families

- `affine_mod`: compute a modular affine dynamical system after `k` steps
- `dfa_shortest`: find the lexicographically first shortest word reaching a target state
- `graph_intervention`: answer reachability after deleting a specified edge
- `boolean_count`: count satisfying assignments of a generated Boolean formula
- `program_trace`: execute a small register machine exactly
- `counterexample_search`: find the smallest integer satisfying generated constraints
- `string_rewrite`: run a simultaneous circular string rewrite system
- `grid_checksum`: follow wrapped grid moves and compute a checksum

Each task is cheap for the verifier and nontrivial for a language model that
must infer and execute the reasoning from a fresh prompt.

## Model Studies

LiveProof can run model submissions through NVIDIA's OpenAI-compatible API when
keys are configured in `.env`. Results are appended incrementally as JSONL and
can be resumed without repeating completed `(model, task)` pairs.

```bash
liveproof eval --tasks corpus/ladder_easy_private.jsonl \
  --models openai/gpt-oss-120b \
  --limit 8 \
  --out corpus/results.jsonl

liveproof report --results corpus/results.jsonl --out corpus/results.md
```

Primary scoring is always deterministic verifier acceptance, not model judgment.

## Packaging

Create a sanitized release archive:

```bash
scripts/package_release.sh liveproof-rc-v1-frontier-v2
```

The archive excludes `.env`, virtual environments, caches, and exploratory
non-RC runs. See `RELEASE_MANIFEST.md` for exact contents.

Create public GitHub and scientific supplement artifacts:

```bash
scripts/build_publication.sh
```

This produces a public repository package without private corpora and a separate
supplement package containing the frozen full release archive for reviewer
reproducibility.

## Citation

Use `CITATION.cff` for software citation metadata. The preprint draft is in
`docs/preprint.md`.
