# LiveProof Ladder Study v1

## Status

This is the first difficulty-ladder study using LiveProof's verifier-backed
protocol.

No model judge was used. Every answer was checked by deterministic code.

## Corpus

Base seed:

```text
2026-05-25-ladder-v1
```

Corpus hashes:

```text
easy   31adaf620cf25527413494f68eb8075d5d183d640bd2eec6c9c866a4f748d49f
medium 788b9eb8a8a61779b70031dd84b3773c0c7e52cf167d0aa660d246655835baa7
hard   c58f945da6c3fd9b61e742a9d8816afead1ffdf801df1834accce87d08bc9e8d
```

Study result:

```text
corpus/ladder_study_8x2x3_20260525T062330Z.results.jsonl
corpus/ladder_study_8x2x3_20260525T062330Z.md
```

## Models

- `openai/gpt-oss-120b`
- `meta/llama-4-maverick-17b-128e-instruct`

`deepseek-ai/deepseek-v4-flash` was excluded from the completed ladder run
because the endpoint stalled before producing usable incremental records during
the ladder attempt. Earlier easy-profile canaries are preserved separately.

## Overall Result

| Model | Accepted | Rejected | Errors | Total | Acceptance |
| --- | ---: | ---: | ---: | ---: | ---: |
| `meta/llama-4-maverick-17b-128e-instruct` | 10 | 13 | 1 | 24 | 42% |
| `openai/gpt-oss-120b` | 8 | 16 | 0 | 24 | 33% |

## Difficulty Curve

| Model | Easy | Medium | Hard |
| --- | ---: | ---: | ---: |
| `meta/llama-4-maverick-17b-128e-instruct` | 4/8 | 3/8 | 3/8 |
| `openai/gpt-oss-120b` | 3/8 | 2/8 | 3/8 |

## Family Profile

| Model | `affine_mod` | `boolean_count` | `dfa_shortest` | `graph_intervention` |
| --- | ---: | ---: | ---: | ---: |
| `meta/llama-4-maverick-17b-128e-instruct` | 0/6 | 2/6 | 2/6 | 6/6 |
| `openai/gpt-oss-120b` | 0/6 | 0/6 | 2/6 | 6/6 |

## Finding

The key finding is not that one model "wins." The important signal is the shape
of the failures:

> Fresh verifier-backed tasks expose structured algorithmic blind spots that
> are invisible in a single aggregate benchmark score.

Both evaluated models solved graph reachability reliably across easy, medium,
and hard profiles. Both collapsed on modular affine recurrence. Boolean counting
and DFA shortest-word tasks showed partial, model-specific capability.

This supports the LiveProof thesis: post-training generated tasks plus exact
verifiers can produce actionable capability profiles from small studies.

## Methodological Notes

- Empty model content is counted as rejected if the API call itself succeeded.
- API transport failures are counted separately as errors.
- The result JSONL includes prompt, task hash, model answer, verifier note, and
  task profile for each record.
- The public corpus contains prompts and verifier hashes; private corpus
  contains verifier payloads for reproducibility.

## Next Study

The next high-value extension is adversarial family design, not larger raw
sample size:

1. Add `scratchpad_resistant_arithmetic`: arithmetic tasks where common
   shortcut heuristics fail.
2. Add `counterexample_search`: find a small object satisfying constraints.
3. Add `program_trace`: trace a short deterministic program with hidden tests.
4. Add `metamorphic_pair`: paired tasks where answers must obey an invariant.

The publication target should be a technical note:

```text
Static Benchmarks Are Dead:
Verifier-Backed Post-Training Evals Reveal Structured Algorithmic Blind Spots
```

