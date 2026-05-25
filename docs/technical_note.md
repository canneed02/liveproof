# Static Benchmarks Are Dead

## Abstract

Frontier AI evaluation is increasingly dominated by public, finite benchmarks.
This creates a structural failure mode: once a benchmark is public, reused, and
important enough to optimize against, score improvements no longer cleanly
measure the intended latent capability. LiveProof proposes a replacement:
post-training, seed-generated, verifier-backed tasks. The model sees only a
fresh task instance; the evaluator checks answers with deterministic verifiers
instead of model judges.

## Claim

No fixed finite public benchmark can remain a reliable standalone measure of a
frontier model capability under adaptive training and repeated public
optimization.

## Argument

Let `B = {x_1, ..., x_n}` be a fixed public benchmark and `s(f, B)` a score for
model `f`. Suppose model builders can observe `B`, observe scores, and update
training, filtering, prompting, tools, or scaffolds to improve `s`. Then the
optimization target is not the latent capability `C`; it is the finite mapping
from benchmark inputs to accepted outputs. For any target score on `B`, there is
a system that implements a lookup table or benchmark-specific heuristic that
achieves that score without acquiring `C` outside `B`. Therefore, score on `B`
alone cannot identify `C`.

This is not a claim that every benchmark score is useless. It is a claim that a
fixed finite public benchmark cannot, by itself, distinguish genuine capability
from benchmark adaptation once the benchmark becomes an optimization target.

## LiveProof Protocol

1. Publish the task generator, verifier, and scoring rules.
2. Commit to a future seed after the evaluated model snapshot exists.
3. Generate task instances from that seed.
4. Give the model public prompts only.
5. Verify submitted answers with deterministic checkers.
6. Publish the seed, task hashes, transcripts, answers, and verifier results.

## Security Properties

LiveProof does not make evaluation impossible to game. It narrows the attack
surface:

- memorizing a fixed benchmark no longer helps
- model-judge bias is removed from primary scoring
- generation and verification are reproducible
- failures can be inspected task by task
- task families can be expanded without changing the protocol

## Why This Matters

The frontier labs already rely on evaluations for deployment decisions, safety
thresholds, and capability claims. If those evaluations are static, saturated,
or contaminated, the measurement layer becomes the weak link. LiveProof targets
that layer directly.

