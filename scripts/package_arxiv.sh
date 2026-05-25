#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p paper/dist
rm -f paper/dist/arxiv-liveproof-v0.1.0.tar.gz

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cp paper/main.tex "$tmp/main.tex"
tar -C "$tmp" -czf paper/dist/arxiv-liveproof-v0.1.0.tar.gz main.tex
digest="$(shasum -a 256 paper/dist/arxiv-liveproof-v0.1.0.tar.gz | awk '{print $1}')"
printf '%s  %s\n' "$digest" "arxiv-liveproof-v0.1.0.tar.gz" > paper/dist/arxiv-liveproof-v0.1.0.tar.gz.sha256

echo "archive=paper/dist/arxiv-liveproof-v0.1.0.tar.gz"
cat paper/dist/arxiv-liveproof-v0.1.0.tar.gz.sha256
