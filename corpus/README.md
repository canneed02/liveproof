# Corpus Policy

LiveProof uses a public/private corpus split.

Public files contain prompts and task hashes:

```text
*_public.jsonl
```

Private files contain verifier payloads and canonical answers:

```text
*_private.jsonl
*.answers.jsonl
```

For a public GitHub repository, commit public corpus files and model result
files. For scientific reproducibility, attach the full frozen release archive as
a supplement so reviewers can audit every verifier-backed answer.

Do not use a published private corpus as a future hidden leaderboard.
