# LiveProof Ladder Protocol

The ladder protocol measures model behavior across task families and difficulty
profiles with deterministic verification.

## Procedure

1. Choose a base seed after the evaluated model snapshots are already available.
2. Generate three corpora from the same base seed:
   - `easy`
   - `medium`
   - `hard`
3. Audit every corpus locally with built-in solvers.
4. Run model submissions with incremental JSONL logging.
5. Verify every answer deterministically.
6. Report a curve:

```text
model x profile x family -> accepted / total
```

## Why a Ladder

A single score hides the interesting information. A model that scores 50% might
be uniformly mediocre, or it might be excellent at reachability and broken at
modular recurrence. The ladder exposes where capability collapses.

## Publication Standard

A public LiveProof study should include:

- base seed
- public corpus files
- corpus hashes
- model identifiers
- result JSONL
- Markdown report
- code commit or archive hash
- no model-judge scoring in primary metrics

## Current Task Families

- `affine_mod`
- `dfa_shortest`
- `graph_intervention`
- `boolean_count`
- `program_trace`
- `counterexample_search`
- `string_rewrite`
- `grid_checksum`
