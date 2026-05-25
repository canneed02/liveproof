# LiveProof Frontier v2

## Purpose

LiveProof RC v1 proved the protocol. Frontier v2 raises the ceiling.

The main addition is an `extreme` profile for all eight task families. The goal
is to keep the benchmark informative if stronger frontier models saturate
`easy`, `medium`, or `hard`.

## Extreme Profile

The `extreme` profile increases the state horizon while preserving exact local
verification:

- `affine_mod`: hundreds of modular recurrence steps over larger primes
- `dfa_shortest`: larger automata with five-symbol alphabets
- `graph_intervention`: larger sparse DAGs
- `boolean_count`: larger CNF instances
- `program_trace`: long register-machine traces
- `counterexample_search`: larger bounded witness search
- `string_rewrite`: long simultaneous circular rewrite dynamics
- `grid_checksum`: long wrapped paths over larger grids

## Method

The test remains raw-answer and verifier-backed:

```text
<answer>FINAL</answer>
```

No model judge is used. If a model emits no answer despite successful transport,
the result is rejected, not counted as an API error.

## Intended Use

Use v2 when a frontier model approaches saturation on RC v1:

```text
easy -> medium -> hard -> extreme
```

The target output is not one score. It is the collapse curve:

```text
model x family x difficulty -> verifier acceptance
```

## DeepSeek V4 Pro Extreme Result

Corpus:

```text
seed: 2026-05-25-frontier-v2
profile: extreme
tasks: 80
hash: 024fd02a3ebc131519a663fd93941a201240698e3b26ec92c3633f28fa67a9c0
```

Study files:

```text
corpus/deepseek_v4_pro_v2_extreme_80_20260525T191654Z.results.jsonl
corpus/deepseek_v4_pro_v2_extreme_80_20260525T191654Z.md
```

Result:

| Model | Profile | Accepted | Total | Acceptance |
| --- | --- | ---: | ---: | ---: |
| `deepseek-v4-pro` | `extreme` | 12 | 80 | 15% |

Family profile:

| Family | Accepted | Total |
| --- | ---: | ---: |
| `affine_mod` | 0 | 10 |
| `boolean_count` | 0 | 10 |
| `counterexample_search` | 1 | 10 |
| `dfa_shortest` | 1 | 10 |
| `graph_intervention` | 10 | 10 |
| `grid_checksum` | 0 | 10 |
| `program_trace` | 0 | 10 |
| `string_rewrite` | 0 | 10 |

Interpretation:

```text
RC v1 distinguishes strong models. Frontier v2 establishes a higher ceiling:
DeepSeek V4 Pro drops from 75% easy / 50% medium / 12% hard on RC v1 to 15% on
the full v2 extreme corpus.
```

This is the desired behavior for a frontier-grade ladder: it avoids saturation
while keeping every failure locally reproducible. The full run also exposes a
useful asymmetry: `graph_intervention` remains easy for the model, while six of
the other seven families are at or near zero.
