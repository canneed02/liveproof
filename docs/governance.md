# Governance Hardening

LiveProof uses automation, but public scientific claims require enforceable
gates.

## Required Gates

- CI must pass before merge.
- `main` must be protected.
- Private corpora must not appear in public branches.
- Secrets must not appear in code, docs, issues, PRs, or artifacts.
- PRs must classify claims as measured, replicated, hypothesis, estimate, or
  speculation.
- Human approval is required for final releases, arXiv submissions, conference
  submissions, and Hacker News posts.

## CI Scope

The CI gate runs:

```bash
scripts/ci_hygiene.sh
```

This performs:

- Python compile check
- unit tests
- private corpus hygiene check
- `.env` exclusion check
- API-key pattern scan

## Branch Policy

Autonomous systems may push branches named:

```text
agent/*
```

They must not push directly to `main`.

## Incident Response

If a gate fails or a secret/private corpus leaks:

1. stop affected automation
2. preserve logs
3. rotate credentials if needed
4. write an incident report
5. patch the root cause
6. re-run clean-clone reproduction
