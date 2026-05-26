# LiveProof Autonomous Research Institute

## Mission

Build an autonomous research institution that continuously discovers, tests,
audits, writes, and publishes verifier-backed AI evaluation research.

The system is not a chatbot loop and not a content farm. It is a scientific
machine with memory, tools, experiments, review, reproducibility, and public
accountability.

The long-term target is to produce research artifacts that are strong enough to
matter to frontier AI labs:

- new benchmark protocols
- new verifier-backed task families
- empirical model reliability maps
- formal arguments about benchmark decay
- reproducible papers, reports, and releases
- public lab notes with raw artifacts and limitations

## Non-Negotiable Principles

1. Evidence before claims.
2. Verifiers before model judges.
3. Fresh seeds before static leaderboards.
4. Reproducibility before publicity.
5. Skeptic review before publication.
6. Public logs over hidden magic.
7. Bot identity must be explicit when the system publishes autonomously.
8. No false authorship, no fake human behavior, no unverifiable grand claims.

## North Star

The institute should eventually operate like a small autonomous lab:

```text
discover problem -> form hypothesis -> build experiment -> run evaluation
-> audit -> replicate -> write -> review -> publish -> absorb feedback
```

Every cycle must leave durable artifacts:

```text
seed
code diff
corpus hash
raw model outputs
verifier result
audit log
skeptic review
claim boundary
next experiment
```

## Autonomy Levels

### Level 1: Autonomous Experiment Runner

Current foundation.

Capabilities:

- generate fresh corpora
- run NVIDIA model evaluation
- audit tasks
- create Markdown ledgers
- push `agent/...` branches
- open draft PRs through a human-operated GitHub token

Not enough:

- no code mutation
- no independent research direction
- no paper writing loop
- no autonomous publication policy

### Level 2: Autonomous Research Engineer

Target next phase.

Capabilities:

- propose code changes
- create new task families
- mutate difficulty profiles
- write tests
- run reproducibility gates
- push draft PRs with self-review

Required gates:

- unit tests pass
- corpus audit pass
- secret scan pass
- private corpus excluded from public branch
- skeptical review included in PR body

### Level 3: Autonomous Paper Builder

Capabilities:

- synthesize results across runs
- maintain paper drafts
- generate tables and claims
- write limitations
- update release notes
- create draft releases

Required gates:

- every table backed by JSONL
- every claim backed by a reproducible command
- every result has a corpus hash
- every paper draft has a limitations section

### Level 4: Autonomous Public Lab

Capabilities:

- publish public lab notes
- maintain GitHub Pages or docs/lab-notes
- announce new branches/releases inside the repo
- summarize negative results

Allowed publication:

- lab notes
- reproducibility ledgers
- draft technical reports

Not allowed without explicit human approval:

- arXiv final submission
- Hacker News post
- conference submission
- claims of solving major open problems

### Level 5: Autonomous Scientific Entity

Long-term target.

Capabilities:

- stable bot identity
- signed commits
- signed artifacts
- public constitution
- machine-readable provenance
- reproducible research archive
- automated public feedback ingestion

Hard requirement:

The system must disclose autonomous generation. It must not impersonate a human
researcher.

## Core Agent Roles

### Director Agent

Owns the research portfolio.

Inputs:

- previous ledgers
- open PRs
- failed experiments
- publication roadmap
- model budget

Outputs:

- prioritized research goals
- cycle plan
- budget allocation
- stop conditions

### Problem Scout

Finds candidate problems.

Sources:

- internal ledgers
- failed task families
- repo issues
- recent model behavior
- published benchmarks
- formal methods opportunities

Output format:

```text
problem
why it matters
testable hypothesis
expected artifact
risk of triviality
```

### Hypothesis Agent

Converts ideas into measurable claims.

Good hypothesis:

```text
If task family X is composed with invariant Y, then model class Z will fail at
profile P while verifier cost remains under threshold T.
```

Bad hypothesis:

```text
This will shock the world.
```

### Builder Agent

Writes implementation changes.

Allowed work:

- task generator changes
- verifier changes
- report generation changes
- harness improvements
- tests
- docs tied to code changes

Must not:

- remove safety gates
- loosen verifier checks to improve scores
- commit secrets
- modify publication policy without a separate policy PR

### Experiment Agent

Runs controlled evaluations.

Rules:

- fixed seed
- fixed model list
- fixed prompt contract
- fixed budget
- JSONL raw outputs
- resumable execution
- no silent discarded failures

### Verifier Agent

Audits correctness.

Checks:

- deterministic generation
- no duplicate task IDs
- local solver/verifier agreement
- public/private split
- corpus hash
- parser ambiguity

### Skeptic Agent

Attacks the claim.

Required questions:

- Is this just a prompt formatting artifact?
- Is the task too synthetic to support the claim?
- Did the model fail due to output contract confusion?
- Is the family profile stable across seeds?
- Could public/private leakage explain the result?
- Are we overstating a small sample?

### Replication Agent

Rebuilds from zero.

Procedure:

```text
fresh clone
install
run tests
rebuild corpus
audit
regenerate report
compare hashes
secret scan
```

### Paper Agent

Writes scientific artifacts.

Allowed:

- draft paper sections
- tables
- limitations
- related-work TODOs
- reproducibility appendix

Must label:

- measured result
- estimate
- hypothesis
- speculation

### Release Agent

Prepares public artifacts.

Allowed:

- draft release notes
- release asset staging
- checksum generation
- draft PRs
- lab-note publication if gates pass

Not allowed by default:

- final GitHub release
- arXiv submission
- Hacker News submission
- main branch merge

## Research Targets

### Target A: Frontier v3 Task Evolution

Goal:

Make task families adaptive enough that model strengths are mapped rather than
flattened.

Initial attack:

- fix `graph_intervention` saturation
- build composite families
- add hidden invariants
- add verifier-cheap, solver-hard structures

Candidate families:

- graph reachability plus checksum path constraint
- DFA shortest path plus modular accumulator
- program trace plus invariant query
- Boolean counting plus witness extraction
- string rewrite plus automaton acceptance

### Target B: Benchmark Decay Theory

Goal:

Turn "static benchmarks decay" into precise claims.

Deliverables:

- theorem statements
- formal models
- impossibility sketches
- simulation artifacts
- examples of benchmark-specific adaptation

### Target C: Proof-Carrying Evaluations

Goal:

Every generated task can carry a compact independent verification path.

Approach:

- deterministic verifier
- optional proof trace
- proof checker
- machine-readable manifest

### Target D: Model Reliability Cartography

Goal:

Map models by family, difficulty, seed, prompt contract, and collapse curve.

Primary output:

```text
model x task_family x difficulty x seed -> verifier acceptance
```

Do not collapse this into a single leaderboard unless required.

### Target E: Autonomous Formalization

Goal:

Bridge empirical failures to formal claims.

Tools to consider later:

- SMT
- SAT
- Lean
- Coq
- property-based testing

## Artifact Hierarchy

Every run belongs to exactly one tier.

### Tier 0: Internal Run

Stored only in server state.

Use for:

- failed experiments
- malformed outputs
- budget tests

### Tier 1: Branch Artifact

Pushed to `agent/...`.

Requirements:

- public corpus
- result JSONL
- report
- ledger

### Tier 2: Draft PR

Requirements:

- Tier 1 complete
- skeptic notes
- reproducibility checklist
- no private corpus

### Tier 3: Lab Note

Autonomous public publication may be allowed once implemented.

Requirements:

- Tier 2 complete
- at least one independent replication
- negative results included
- clear claim boundary
- autonomous-authorship disclosure

### Tier 4: Technical Report Release

Requires human approval unless policy changes later.

Requirements:

- frozen corpus
- supplement archive
- checksum
- clean clone reproduction
- release notes

### Tier 5: arXiv or Conference

Human gate required.

No exception until the institute has a long record of reliable lab-note output.

## Memory System

The institute must remember:

- run metadata
- corpus hashes
- claims tested
- failures
- accepted/rejected PRs
- model behavior by family
- reviewer objections
- publication outcomes

Minimum memory stores:

```text
SQLite: structured run metadata
Git: public artifact history
Markdown ledgers: human-readable context
JSONL: raw model outputs
Private state dir: private verifier payloads
```

Future memory stores:

```text
embedding index for ledgers
claim graph
model-family matrix
paper draft history
review objection database
```

## Compute Policy

The system should exploit available compute aggressively but not blindly.

Budget rules:

- hard per-cycle request cap
- hard per-day request cap
- exponential backoff on provider errors
- automatic degradation to smaller model set on repeated errors
- no unbounded API loops
- no retry storms

Evaluation priority:

1. cheap local verifier tests
2. small model canaries
3. limited frontier slices
4. full corpus only after canary signal

## Publication Constitution

No public claim may be made unless it is classified:

```text
measured
replicated
hypothesis
estimate
speculation
```

Forbidden:

- "solved" without reproducible proof
- "best model" without defined benchmark scope
- "AGI" without operational definition
- "world-changing" as a scientific claim
- hiding negative results that contradict the central claim

Required in every public note:

- exact seed
- exact model IDs
- exact task count
- raw result location
- verifier method
- limitations
- authorship disclosure

## Security Model

Secrets:

- never committed
- never printed in ledgers
- never copied into release archives

GitHub:

- deploy key scoped to one repo
- branch prefix only by policy
- main protected at GitHub level before higher autonomy
- no force push
- no tag deletion

Server:

- runtime repo separated from legacy repo
- private corpora outside public repo
- systemd logs monitored
- failure files saved

## Main Branch Protection Requirement

Before Level 2 is enabled, GitHub must protect `main`:

- require PR before merge
- block force pushes
- block deletions
- restrict direct pushes if possible
- require status checks once CI exists

This is not optional. Level 2 writes code; code-writing autonomy without branch
protection is unacceptable.

## Definition of Success

The project is succeeding if, every week, it produces:

- at least one audited research branch
- at least one nontrivial negative result
- at least one proposed task or protocol improvement
- no leaked secrets
- no unsupported public claims
- a clearer map of model failure modes

The project is failing if it produces:

- many claims without artifacts
- repeated trivial benchmark variants
- unreproducible reports
- public hype without limitations
- unreviewed changes to main

## Immediate Next Step

Implement Level 2 planning only after this document is accepted:

```text
Autonomous Research Engineer:
- code mutation proposals
- isolated worktree per branch
- tests
- skeptic review
- draft PR
```

No code-writing autonomy should be enabled until:

- `main` branch protection exists
- CI exists
- foundry branches are isolated from previous runs
- private corpus exclusion is enforced by tests
- secret scanning runs in CI

