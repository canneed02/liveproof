# Short Public Announcement

I released LiveProof v0.1.0, a verifier-backed post-training evaluation protocol
for AI models.

The mechanism is simple:

1. publish the generator and verifier
2. choose a seed after the model snapshot exists
3. generate fresh tasks
4. score raw answers with deterministic verifiers

Initial measured result:

```text
deepseek-v4-pro on Frontier v2 extreme: 12/80 accepted, 15%, 0 API errors
```

The family profile is the interesting part:

```text
graph_intervention      10/10
dfa_shortest             1/10
counterexample_search    1/10
all other families       0/10
```

Repository:

```text
https://github.com/canneed02/liveproof
```

Release:

```text
https://github.com/canneed02/liveproof/releases/tag/v0.1.0-rc1-frontier-v2
```
