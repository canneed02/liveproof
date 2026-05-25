# Security Policy

## Secrets

Do not commit `.env`, provider API keys, private credentials, virtual
environments, shell histories, or raw machine-specific configuration. The release
packaging workflow scans publication artifacts for common API-key patterns.

## Private Corpus Handling

Files named `*_private.jsonl` contain verifier payloads and answers. They are
safe for reproducibility supplements, but they should not be treated as hidden
benchmark material after publication.

## Reporting Issues

For security-sensitive reports, include:

- affected file or command
- reproduction steps
- whether the issue leaks secrets, corrupts scoring, or changes verifier output
- proposed minimal fix, if known

Do not include live API keys or provider credentials in issue text.
