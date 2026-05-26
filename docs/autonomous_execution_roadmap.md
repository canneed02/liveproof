# Autonomous Research Execution Roadmap

## Purpose

This roadmap converts the LiveProof Autonomous Research Institute plan into
execution phases. It is a planning document, not implementation.

The strategy is to raise autonomy only when evidence shows the previous level is
stable. The goal is maximum ambition with minimum uncontrolled blast radius.

## Current Baseline

Implemented foundation:

- public LiveProof repository
- verifier-backed task generator
- RC v1 and Frontier v2 artifacts
- NVIDIA-based server foundry
- systemd timer
- deploy key scoped to one GitHub repository
- branch-based autonomous ledgers
- first autonomous draft PR

Known limitations:

- no CI yet
- no branch protection verified
- no automatic PR creation from server
- no code-writing autonomy
- no autonomous lab-note publishing
- no multi-agent internal review loop

## Phase 0: Stabilize the Current Foundry

Goal:

Make the current Level 1 loop boringly reliable.

Deliverables:

- daily foundry health check
- failure classification
- request budget accounting
- branch cleanup policy
- run database schema documented
- dashboard or summary command

Exit criteria:

- seven consecutive scheduled cycles without secret leakage
- failures produce readable failure files
- every completed run has ledger, JSONL, report, and public corpus
- timer survives reboot

## Phase 1: Governance Hardening

Goal:

Make GitHub and publication boundaries enforceable.

Deliverables:

- GitHub branch protection for `main`
- no direct pushes to `main`
- CI workflow for tests and secret scan
- PR template requiring claim classification
- issue template for research hypotheses
- CODEOWNERS or equivalent human review gate

Required CI checks:

```text
unit tests
python compile
secret scan
public package hygiene
no private corpus in public branch
```

Exit criteria:

- bot cannot accidentally merge to `main`
- bot cannot pass PR with private corpus
- every PR exposes exact artifacts changed

## Phase 2: Autonomous Research Engineer

Goal:

Let the system propose code changes safely.

New capabilities:

- create isolated worktree
- select one mutation objective
- edit generator/verifier/report code
- add tests
- run local gates
- commit branch
- open draft PR

Allowed mutation classes:

- new task family
- harder profile
- stricter answer parser
- report table improvement
- corpus manifest improvement
- verifier ambiguity test

Forbidden mutation classes:

- relaxing verifier correctness
- deleting tests
- removing secret scan
- modifying branch protection docs without explicit policy PR
- changing publication constitution inside a research PR

Required PR sections:

```text
Hypothesis
Code Changes
Experiment
Results
Skeptic Review
Reproduction
Limitations
```

Exit criteria:

- three code-writing PRs created without leaking secrets
- at least one PR produces a useful negative result
- at least one PR improves a task family or verifier
- human review can understand the diff in under 15 minutes

## Phase 3: Multi-Agent Review Loop

Goal:

Make the system adversarial toward its own claims.

Agents:

- Builder
- Experimenter
- Verifier
- Skeptic
- Replicator
- Paper Writer

Required flow:

```text
Builder writes change
Experimenter runs it
Verifier audits it
Skeptic attacks it
Replicator rebuilds it
Paper Writer summarizes it
Release Agent opens PR
```

Exit criteria:

- every PR includes a skeptic objection section
- every accepted claim has a replication log
- at least 30% of candidate claims are rejected internally

Why rejection rate matters:

If the system never rejects its own claims, it is not doing science. It is
producing marketing.

## Phase 4: Autonomous Lab Notes

Goal:

Allow public publication of low-risk, clearly labeled lab notes.

Permitted auto-publication target:

```text
docs/lab-notes/YYYY-MM-DD-topic.md
```

Lab notes may include:

- failed experiments
- small measured results
- task family analysis
- reproducibility observations
- future hypotheses

Lab notes must include:

- autonomous authorship disclosure
- raw artifact links
- exact seed
- exact model IDs
- exact limitations
- no grand claims

Exit criteria:

- ten lab notes published without correction for factual error
- at least three negative results published
- public feedback is tracked in issues

## Phase 5: Technical Report Draft Releases

Goal:

Let the system prepare full report releases, but not final publish without gate.

Capabilities:

- update preprint draft
- create release candidate archive
- generate supplement
- generate checksums
- open draft release notes
- open PR for report

Human gate remains required for:

- final GitHub release publication
- arXiv submission
- conference submission
- Hacker News announcement

Exit criteria:

- release candidate can be reproduced from clean clone
- all tables backed by raw JSONL
- all claims classified
- limitations included

## Phase 6: Autonomous Public Research Entity

Goal:

Turn the system into a durable public scientific actor.

Required before entry:

- signed bot commits
- public bot identity
- public constitution
- issue-based feedback loop
- correction policy
- retraction policy
- artifact DOI process

Allowed:

- publish lab notes
- publish weekly digests
- maintain reproducibility index
- respond to issues with draft answers

Still human-gated:

- final arXiv submission
- major press/social launches
- claims of solving major open problems

## Phase 7: Grand Challenge Program

Goal:

Aim the institute at hard problems without destroying rigor.

Grand challenge classes:

### Class A: Engineering Open Problems

Timeline:

```text
hours to days
```

Examples:

- better verifier-backed eval harness
- stronger corpus split policy
- better report generation

### Class B: Empirical Science

Timeline:

```text
days to weeks
```

Examples:

- model collapse curves
- family-specific reliability maps
- seed sensitivity studies

### Class C: Formal Micro-Problems

Timeline:

```text
weeks
```

Examples:

- verifier correctness lemmas
- benchmark decay toy theorem
- proof-carrying task format

### Class D: Serious Research Problems

Timeline:

```text
months
```

Examples:

- adaptive benchmark theory
- autonomous task evolution
- general verifier-backed evaluation framework

### Class E: Civilization-Scale Problems

Timeline:

```text
unknown
```

Policy:

The institute may formalize subproblems, generate experiments, and maintain
research maps. It must not claim solutions without machine-checkable proofs or
overwhelming reproducible evidence.

## Operating Metrics

Weekly metrics:

- cycles completed
- cycles failed
- API error rate
- accepted/rejected model results
- new branches
- draft PRs
- internal claim rejection rate
- reproduction pass rate
- secret scan pass rate

Research quality metrics:

- number of claims downgraded by Skeptic
- number of negative results preserved
- number of task families improved
- number of external issues/comments addressed
- number of artifacts reproducible from clean clone

## Stop Conditions

The system must pause higher autonomy if:

- any secret leaks
- private corpus appears in public branch
- branch protection is bypassed
- PRs become unreadable
- API cost exceeds budget
- public note contains unsupported claim
- reproducibility falls below threshold

Pause means:

```text
disable code-writing autonomy
keep logging
require human review
write incident report
fix root cause
```

## First 30 Days

Week 1:

- stabilize Level 1
- add CI and branch protection
- document current foundry output

Week 2:

- implement Level 2 code mutation in dry-run mode
- no auto PR until local gates pass
- create first task-family mutation proposal

Week 3:

- enable draft PR creation for code-writing agent
- add Skeptic section to every PR
- run first replicated task-family experiment

Week 4:

- publish first autonomous lab note if gates pass
- prepare Frontier v3 release candidate proposal
- decide whether to expand model budget

## First 90 Days

By day 90, the institute should have:

- a stable autonomous run history
- multiple task family improvements
- at least one strong Frontier v3 candidate
- a model reliability map across several NVIDIA-hosted models
- a paper draft with new measured results
- a public lab-note archive
- zero secret leaks
- zero unsupported public claims

## Decision Rule

Raise autonomy only when the previous level has demonstrated reliability.

No exception for ambition. The project is allowed to be extreme, but it must not
be sloppy.

