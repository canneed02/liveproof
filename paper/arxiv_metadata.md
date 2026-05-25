# arXiv Submission Metadata Draft

Title:

```text
Static Benchmarks Are Dead: Verifier-Backed Post-Training Evals Reveal Structured Algorithmic Blind Spots
```

Authors:

```text
Nguyen Thanh Phi Long
```

Suggested primary category:

```text
cs.AI
```

Suggested cross-lists:

```text
cs.LG
cs.CL
```

Abstract:

```text
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
```

Comments:

```text
Initial release candidate. Code, corpora, model transcripts, and reproducibility supplement: https://github.com/canneed02/liveproof
```

License recommendation:

```text
arXiv.org perpetual, non-exclusive license to distribute
```

Submit package:

```text
paper/arxiv-liveproof-v0.1.0.tar.gz
```

Notes:

- First-time arXiv submitters may need endorsement in the chosen category.
- Preview the generated PDF before final submit.
- If arXiv asks for the top-level file, use `main.tex`.
