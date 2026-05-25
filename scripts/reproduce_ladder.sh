#!/usr/bin/env bash
set -euo pipefail

seed="${1:-2026-05-25-ladder-v1}"
count="${2:-40}"

cd "$(dirname "$0")/.."

for profile in easy medium hard; do
  private="corpus/ladder_${profile}_private.jsonl"
  public="corpus/ladder_${profile}_public.jsonl"
  answers="corpus/ladder_${profile}.answers.jsonl"

  liveproof generate \
    --seed "$seed" \
    --profile "$profile" \
    --count "$count" \
    --out "$private" \
    --public-out "$public"

  liveproof audit --tasks "$private"
  liveproof solve --tasks "$private" --out "$answers"
  liveproof verify --tasks "$private" --answers "$answers"
done

