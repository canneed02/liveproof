# Hacker News Launch Draft

Recommended submission type:

```text
Show HN
```

Recommended URL:

```text
https://github.com/canneed02/liveproof
```

Recommended title:

```text
Show HN: LiveProof, verifier-backed post-training evals for AI models
```

Do not use:

```text
Static Benchmarks Are Dead
```

That title is strong for the paper, but it is too editorialized for Hacker News.

First comment:

```text
I built LiveProof as a small verifier-backed evaluation protocol for testing AI
models on fresh seed-generated algorithmic tasks.

The main idea is to publish the generator and verifier, then instantiate tasks
from a seed after the model snapshot exists. Answers are scored by deterministic
local verifiers, not by a model judge.

The current release includes eight task families, public/private corpus splits,
raw JSONL model transcripts, and a reproducibility supplement.

Measured result so far:

deepseek-v4-pro on Frontier v2 extreme: 12/80 accepted, 15%, 0 API errors.

The interesting part is the family profile: it solved graph_intervention 10/10,
but scored 0/10 on affine_mod, boolean_count, grid_checksum, program_trace, and
string_rewrite.

I would especially like criticism on the protocol design: seed timing, public vs
private corpus handling, and whether the task families are too synthetic or
usefully diagnostic.
```

Submission checklist:

- Submit the GitHub repo, not the release asset.
- Stay online for the first 1-2 hours to answer technical questions.
- Do not ask anyone for upvotes.
- Do not overclaim that this is a complete AI benchmark.
- If challenged, emphasize that this is a release candidate and a protocol
  artifact, not a final leaderboard.
