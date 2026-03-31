# PA·co State Management Schema

> In v2, the dispatch system evolves into state-based coordination. Products track their own state. A global pipeline tracks all products.

## Directory Structure

```
state/
  PIPELINE.md          — All products and their current phases
  DISPATCH_TODAY.md    — Today's task assignments (rewritten daily)
  HALT.md              — Emergency stop register
  CEO_BLOCKERS.md      — Items requiring CEO decision

products/{name}/
  CLAUDE.md            — Product-specific rules and context
  STATE.md             — Current progress, bugs, metrics
  BRANDING.md          — Visual identity and brand rules
  DISPATCH.md          — Product-specific task queue
  mvp-specs/           — What to build (from Phase 2: Refine)
```

## PIPELINE.md (max 30 lines)

Tracks ALL products and their current workflow phase.

```markdown
# Pipeline

## Current Week Mode
- mode: SPRINT | CONSOLIDATION
- week_start: YYYY-MM-DD
- next_switch: YYYY-MM-DD

## Active Products
| Product | Phase | Status | Last Updated |
|---------|-------|--------|-------------|
| ProductA | EVOLVE_A | Active, distribution push | 2026-03-30 |

## In Development (max 1 product in phases 1-6)
| Product | Phase | Started | ETA |
|---------|-------|---------|-----|
| ProductB | DEVELOP | 2026-03-25 | 2026-04-05 |
```

**Rule:** Only active products here. Completed/killed products archived to vector DB.

## Product STATE.md (max 40 lines)

Per-product state. Rewritten every session.

```markdown
# [Product Name] — State

## Current Phase
- phase: DEVELOP
- last_actor: "builder" | "qa" | "none" | "ceo_approved"
- last_updated: YYYY-MM-DD
- autonomous_build: false

## Status
- progress: [what's done]
- remaining: [what's left]
- bugs_active: 0
- blockers: none

## Pending Work (Evolve only)
| # | Type | Priority | Description | Source |
|---|---|---|---|---|
| 1 | bug | P0 | Critical auth issue | user report |

## Metrics (Evolve only)
- users: [count]
- revenue: $X MRR
- traffic: [sources]
```

## HALT.md

```markdown
# HALT Status

## Current: CLEAR | ACTIVE

## Active Halts:
| Scope | Reason | Date | Resumed |
|-------|--------|------|---------|

## Rules:
- CEO writes "HALT [product]" or "HALT ALL"
- EVERY schedule reads this FIRST before doing anything
- Persists until CEO writes "RESUME [product]" or "RESUME ALL"
```

## CEO_BLOCKERS.md

Items that require CEO decision. No agent can resolve these.

```markdown
# CEO Blockers

| # | Date | Product | Blocker | Requested By | Status |
|---|------|---------|---------|-------------|--------|
| 1 | 2026-03-31 | ProductA | Spending approval: $29/mo | Governance | PENDING |
```

## DISPATCH_TODAY.md (max 50 lines)

Daily task assignments. Rewritten each morning by the Standup session.

```markdown
# Dispatch — YYYY-MM-DD

## Priority Tasks
| # | Agent | Task | Product | Deadline |
|---|-------|------|---------|----------|

## Schedule Results (today)
| Time | Schedule | Result |
|------|----------|--------|

## CEO Feedback (if any)
[Items CEO communicated that affect today's work]
```

## Build↔QA Alternation

The `last_actor` field in STATE.md controls who works next:

```
Builder works → sets last_actor = "builder" → QA's turn next
QA works → sets last_actor = "qa" → Builder's turn next
```

**Exception:** Autonomous builds (`autonomous_build: true`) skip alternation. Both Builder and QA run every session.

## v1 Dispatch vs v2 State

| v1 (Dispatch) | v2 (State) |
|----------------|------------|
| Department dispatch files | Product STATE.md files |
| Cross-dept via GENERAL.md | Cross-product via PIPELINE.md |
| Activity logs per department | Progress tracked per product |
| Agent heartbeats in dispatch | Agent activity in DISPATCH_TODAY |
| Department-centric coordination | Product-centric coordination |

The v1 dispatch system still works for simpler setups. v2 state management is recommended when you have multiple products in different lifecycle phases.
