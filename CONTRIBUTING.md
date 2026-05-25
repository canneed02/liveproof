# Contributing

LiveProof values narrow, reproducible changes.

Before opening a change:

1. Run the local tests.
2. Run corpus audit for any generated private corpus.
3. Include corpus hashes for any newly published corpus.
4. Keep model claims tied to raw JSONL result files.
5. Avoid adding model-judge scoring to the primary metric.

Required checks:

```bash
python3 -m unittest discover -s tests
liveproof audit --tasks corpus/v2_extreme_private.jsonl
```

For new task families, include:

- deterministic generation from seed
- public prompt record
- private verifier payload
- local solver used for audit
- verifier acceptance and rejection tests
