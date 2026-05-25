# Static Benchmarks Are Dead

## Subtitle

Verifier-Backed Post-Training Evals Reveal Structured Algorithmic Blind Spots

## Abstract

Public static benchmarks are vulnerable to adaptive optimization. Once a fixed
finite benchmark becomes a target for model development, high score no longer
cleanly identifies the latent capability the benchmark was meant to measure.
LiveProof is a post-training evaluation protocol that replaces fixed public
question sets with seed-generated tasks and deterministic verifiers. The
generator, verifier, scoring rules, and corpus hashes are public; only the
future seed and private verifier payloads are withheld until evaluation time.
In an initial release candidate, DeepSeek V4 Pro scores 11/24 on the RC v1
sample and 12/80 on the Frontier v2 extreme corpus, with zero API transport
errors. The result is not a universal model ranking. It is evidence that fresh
verifier-backed tasks expose family-specific algorithmic blind spots that a
single aggregate benchmark score can hide.

## 1. Problem

Frontier AI evaluation increasingly depends on public, finite benchmarks. These
benchmarks are useful while they are new, but their measurement value decays
under repeated exposure. If a benchmark is public, reused, and important enough
to optimize against, then it becomes part of the development environment.

The core failure mode is not simple memorization only. It includes:

- direct benchmark memorization
- benchmark-specific prompting and scaffolding
- data filtering shaped by public benchmark style
- synthetic training curricula optimized toward benchmark distributions
- repeated model selection against known acceptance criteria

The result is a measurement problem: benchmark score becomes an increasingly
ambiguous mixture of capability, adaptation, and contamination.

## 2. Claim

No fixed finite public benchmark can remain a reliable standalone measure of a
frontier model capability under adaptive training and repeated public
optimization.

This claim is deliberately narrow. It does not say benchmark scores are useless.
It says that a fixed public benchmark cannot, by itself, identify a latent
capability once the benchmark is an optimization target.

## 3. Argument

Let `B = {x_1, ..., x_n}` be a fixed public benchmark and let `s(f, B)` be the
score of system `f` on `B`. Suppose builders can observe `B`, observe scores,
and adapt training, filtering, prompting, tools, or model selection to improve
`s`.

The optimization target is then the finite mapping from benchmark inputs to
accepted outputs, not the intended latent capability `C`. For any target score
on `B`, a system can improve by learning benchmark-specific heuristics or a
lookup table over `B` without acquiring `C` outside `B`. Therefore, score on `B`
alone cannot identify `C`.

The remedy is not secrecy alone. A permanently secret static benchmark also
decays if it leaks, is overused, or becomes implicitly optimized through
feedback. The stronger approach is to make the task generator and verifier
public, then instantiate fresh tasks after the evaluated model snapshot exists.

## 4. LiveProof Protocol

LiveProof uses the following protocol:

1. Publish the generator, verifier, scoring rules, and task-family definitions.
2. Commit to evaluating a model snapshot that already exists.
3. Select or reveal a seed after the model snapshot exists.
4. Generate public prompts and private verifier payloads from that seed.
5. Submit model answers in a strict raw-answer format.
6. Score with deterministic local verifiers, not model judges.
7. Publish prompts, hashes, transcripts, verifier results, and the seed.

The protocol is designed so that a model cannot benefit from memorizing a fixed
finite prompt set before the seed is chosen, while reviewers can still reproduce
the corpus and verify every score.

## 5. Task Families

The current artifact includes eight synthetic algorithmic families:

| Family | Capability Probed |
| --- | --- |
| `affine_mod` | modular recurrence execution |
| `dfa_shortest` | shortest-path search in automata |
| `graph_intervention` | reachability after deleting a specified edge |
| `boolean_count` | exact combinatorial counting |
| `program_trace` | register-machine execution |
| `counterexample_search` | smallest satisfying witness search |
| `string_rewrite` | simultaneous circular rewrite dynamics |
| `grid_checksum` | state tracking plus checksum computation |

Each family is generated deterministically from seed material and has an exact
local verifier. The task instances are intended to be cheap for the verifier and
nontrivial for a language model that must execute the reasoning from a fresh
prompt.

## 6. Release Candidate Corpus

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

Frontier v2 extreme corpus hash:

```text
024fd02a3ebc131519a663fd93941a201240698e3b26ec92c3633f28fa67a9c0
```

## 7. Measured Results

DeepSeek V4 Pro RC v1 sample:

| Model | Accepted | Rejected | Errors | Total | Acceptance |
| --- | ---: | ---: | ---: | ---: | ---: |
| `deepseek-v4-pro` | 11 | 13 | 0 | 24 | 46% |

DeepSeek V4 Pro Frontier v2 extreme:

| Model | Accepted | Rejected | Errors | Total | Acceptance |
| --- | ---: | ---: | ---: | ---: | ---: |
| `deepseek-v4-pro` | 12 | 68 | 0 | 80 | 15% |

Frontier v2 family profile:

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

## 8. Interpretation

The most important result is not the aggregate score. It is the structured
failure profile. DeepSeek V4 Pro solves all sampled `graph_intervention` tasks
in the Frontier v2 corpus while failing nearly all other task families. That
asymmetry would be hidden by a single aggregate benchmark score.

The observed collapse from RC v1 to Frontier v2 is also useful. A stronger
future model may saturate easy or medium profiles, but a difficulty ladder with
fresh seed-generated instances can continue to expose where reliability breaks.

## 9. Limitations

LiveProof is not a complete measurement of intelligence or safety. Current
limitations include:

- the task families are synthetic and algorithmic
- the initial model sample is small
- prompts are raw-answer oriented and do not test tool-use workflows
- the current artifact evaluates correctness, not calibration or reasoning trace
  faithfulness
- once private corpora are published, they become reproducibility artifacts, not
  hidden benchmark material

These limitations are intentional boundaries for a release candidate. The
scientific claim is about protocol structure and reproducible verifier-backed
measurement, not universal model ranking.

## 10. Reproducibility

The artifact includes:

- generator and verifier source code
- public corpora
- private corpora in the frozen supplement
- result JSONL files
- Markdown reports
- corpus hashes
- release manifest
- packaging script with secret-scan checks

Primary verification commands:

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

## 11. Conclusion

Static public benchmarks are structurally fragile under adaptive optimization.
LiveProof offers a practical alternative: publish the evaluation mechanism, keep
task instances fresh, and score with deterministic verifiers. The initial
results show that this approach can reveal structured model blind spots even
when aggregate benchmark scores elsewhere appear strong.
