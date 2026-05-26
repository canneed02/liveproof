#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 -m compileall -q src scripts tests
PYTHONPATH=src python3 -m unittest discover -s tests

if find . \
  -path './.git' -prune -o \
  -path './.venv' -prune -o \
  -path './dist' -prune -o \
  -path './publication' -prune -o \
  -name '.env' -print -o \
  -name '*_private.jsonl' -print -o \
  -name '*.answers.jsonl' -print | grep -q .; then
  echo "public hygiene failed: private or secret-like files are present" >&2
  find . \
    -path './.git' -prune -o \
    -path './.venv' -prune -o \
    -path './dist' -prune -o \
    -path './publication' -prune -o \
    -name '.env' -print -o \
    -name '*_private.jsonl' -print -o \
    -name '*.answers.jsonl' -print >&2
  exit 1
fi

if grep -R -E '(n[v]api-|s[k]-[A-Za-z0-9]{20,})' \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude-dir=dist \
  --exclude-dir=publication \
  . >/dev/null; then
  echo "secret scan failed" >&2
  exit 1
fi

echo "ci_hygiene=ok"
