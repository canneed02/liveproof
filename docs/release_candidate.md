# LiveProof Release Candidate v1

## Summary

LiveProof v1 is now a reproducible verifier-backed evaluation artifact.

The release candidate includes:

- eight deterministic task families
- easy/medium/hard difficulty profiles
- public/private corpus split
- corpus hashes
- built-in solvers for audit only
- incremental model evaluation through NVIDIA's OpenAI-compatible API
- deterministic verification with no model judge
- Markdown reports with model x family x difficulty matrices

## Task Families

| Family | Capability Probed |
| --- | --- |
| `affine_mod` | modular recurrence execution |
| `dfa_shortest` | shortest-path search in automata |
| `graph_intervention` | reachability after causal-style intervention |
| `boolean_count` | exact combinatorial counting |
| `program_trace` | register-machine execution |
| `counterexample_search` | smallest satisfying witness search |
| `string_rewrite` | simultaneous rewrite dynamics |
| `grid_checksum` | state tracking plus checksum computation |

## RC Corpus

Base seed:

```text
2026-05-25-rc-v1
```

Corpus size:

```text
80 tasks per profile
240 tasks total
```

Corpus hashes:

```text
easy   6d2ada024c4af2874fda6ff8b2594e07607957c07e088559f528dd2a1ea68296
medium 1260f19e5fced4714478081df4558077b52a4e73b6b56e4e05caa202d5bc315a
hard   fd9f739df08684894274dc84c23f1e12dc27c30750b9ff2bdd39aed822e6b252
```

All three corpora pass local audit.

## RC Study

Result files:

```text
corpus/rc_v1_study_8x2x3_20260525T063550Z.results.jsonl
corpus/rc_v1_study_8x2x3_20260525T063550Z.md
```

Study shape:

```text
8 tasks/profile/model
3 profiles
2 models
48 records
```

Models:

- `openai/gpt-oss-120b`
- `meta/llama-4-maverick-17b-128e-instruct`

Overall:

| Model | Accepted | Rejected | Errors | Total | Acceptance |
| --- | ---: | ---: | ---: | ---: | ---: |
| `deepseek-v4-pro` | 11 | 13 | 0 | 24 | 46% |
| `openai/gpt-oss-120b` | 5 | 19 | 0 | 24 | 21% |
| `meta/llama-4-maverick-17b-128e-instruct` | 3 | 21 | 0 | 24 | 12% |

Family profile:

| Model | `affine_mod` | `boolean_count` | `counterexample_search` | `dfa_shortest` | `graph_intervention` | `grid_checksum` | `program_trace` | `string_rewrite` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `deepseek-v4-pro` | 0/3 | 2/3 | 1/3 | 2/3 | 3/3 | 0/3 | 2/3 | 1/3 |
| `openai/gpt-oss-120b` | 0/3 | 0/3 | 0/3 | 2/3 | 3/3 | 0/3 | 0/3 | 0/3 |
| `meta/llama-4-maverick-17b-128e-instruct` | 0/3 | 1/3 | 0/3 | 0/3 | 1/3 | 0/3 | 1/3 | 0/3 |

Difficulty profile:

| Model | Easy | Medium | Hard |
| --- | ---: | ---: | ---: |
| `deepseek-v4-pro` | 6/8 | 4/8 | 1/8 |
| `openai/gpt-oss-120b` | 2/8 | 2/8 | 1/8 |
| `meta/llama-4-maverick-17b-128e-instruct` | 3/8 | 0/8 | 0/8 |

## Interpretation

This study is intentionally small. Its purpose is not to rank models with high
statistical confidence. Its purpose is to validate the LiveProof protocol and
show that verifier-backed fresh tasks produce structured capability profiles.

The RC signal is strong enough to justify publication as an artifact:

- graph intervention tasks are the most robust family for current models
- DFA shortest-word remains tractable for `openai/gpt-oss-120b`
- modular recurrence, witness search, string rewrite, and grid checksum expose
  sharp failure modes
- medium and hard profiles collapse quickly for the sampled models
- empty model content is treated as a rejected submission when transport
  succeeds, not as a verifier error

## Release Criteria Met

- deterministic generation
- reproducible corpus hashes
- local audit pass
- eight task families
- three difficulty profiles
- model study with raw JSONL records
- public-facing technical notes
- no primary model-judge scoring

## Next Public Step

Publish as:

```text
Static Benchmarks Are Dead:
Verifier-Backed Post-Training Evals Reveal Structured Algorithmic Blind Spots
```

The public claim should be narrow and defensible:

> LiveProof shows how fresh seed-generated tasks with exact verifiers can expose
> structured algorithmic blind spots that aggregate static benchmarks hide.
