# DeepSeek V4 Pro LiveProof Study

## Provider

DeepSeek official OpenAI-compatible API.

Available account models at test time:

```text
deepseek-v4-pro
deepseek-v4-flash
```

The evaluated frontier model was:

```text
deepseek-v4-pro
```

## Corpus

LiveProof RC v1 corpus.

Seed:

```text
2026-05-25-rc-v1
```

Hashes:

```text
easy   6d2ada024c4af2874fda6ff8b2594e07607957c07e088559f528dd2a1ea68296
medium 1260f19e5fced4714478081df4558077b52a4e73b6b56e4e05caa202d5bc315a
hard   fd9f739df08684894274dc84c23f1e12dc27c30750b9ff2bdd39aed822e6b252
```

Study files:

```text
corpus/deepseek_v4_pro_rc_study_8x3_20260525T064933Z.results.jsonl
corpus/deepseek_v4_pro_rc_study_8x3_20260525T064933Z.md
```

## Result

| Model | Accepted | Rejected | Errors | Total | Acceptance |
| --- | ---: | ---: | ---: | ---: | ---: |
| `deepseek-v4-pro` | 11 | 13 | 0 | 24 | 46% |

## Difficulty Curve

| Profile | Accepted | Total | Acceptance |
| --- | ---: | ---: | ---: |
| easy | 6 | 8 | 75% |
| medium | 4 | 8 | 50% |
| hard | 1 | 8 | 12% |

## Family Profile

| Family | Accepted | Total | Acceptance |
| --- | ---: | ---: | ---: |
| `affine_mod` | 0 | 3 | 0% |
| `boolean_count` | 2 | 3 | 67% |
| `counterexample_search` | 1 | 3 | 33% |
| `dfa_shortest` | 2 | 3 | 67% |
| `graph_intervention` | 3 | 3 | 100% |
| `grid_checksum` | 0 | 3 | 0% |
| `program_trace` | 2 | 3 | 67% |
| `string_rewrite` | 1 | 3 | 33% |

## Comparison Against Previous RC Models

| Model | Accepted | Total | Acceptance |
| --- | ---: | ---: | ---: |
| `deepseek-v4-pro` | 11 | 24 | 46% |
| `openai/gpt-oss-120b` | 5 | 24 | 21% |
| `meta/llama-4-maverick-17b-128e-instruct` | 3 | 24 | 12% |

DeepSeek V4 Pro is the strongest model tested so far on the LiveProof RC v1
sample. It preserves nonzero performance on medium tasks and substantially
outperforms the previous two-model RC study.

## Interpretation

The result is strong but not absolute. This is a small sample designed to test
the protocol, not to produce a final leaderboard.

The meaningful finding is the profile:

- `graph_intervention` is solved reliably
- `boolean_count`, `dfa_shortest`, and `program_trace` remain partially robust
- `affine_mod` and `grid_checksum` remain sharp failure families
- performance decays from 75% on easy to 12% on hard

This supports the LiveProof thesis: verifier-backed fresh tasks expose not just
"how much" a model can solve, but where its algorithmic reliability collapses.

## Frontier v2 Follow-up

DeepSeek V4 Pro was also run on the full 80-task v2 `extreme` profile.

```text
corpus/deepseek_v4_pro_v2_extreme_80_20260525T191654Z.md
```

Result:

```text
12/80 accepted, 15%, 0 API errors
```

Family profile:

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

This confirms that v2 is high enough to avoid saturating the strongest tested
model while still preserving family-level signal.
