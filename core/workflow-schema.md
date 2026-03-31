# PA·co Workflow — 7 Phases

> Every product goes through the full 7-phase workflow. No shortcuts. No tiers.

```
RESEARCH → REFINE → POST-REFINE → CEO GATE → DEVELOP → DEPLOY → EVOLVE
```

## Phase Overview

| # | Phase | Purpose | Gatekeeper | Key Output |
|---|-------|---------|------------|------------|
| 1 | Research | Find PROBLEMS, not solutions | PA·co | SPEC_TEMPLATE |
| 2 | Refine | All departments enrich in parallel | PA·co | 6 SPEC_MVP files |
| 3 | Post-Refine | Audit all specs. Fix or kill. | Argus (Auditor) | Audit report: GO/KILL |
| 4 | CEO Gate | CEO approves, rejects, or defers | CEO | GO / NO-GO / DEFER |
| 5 | Develop | Build from specs. No improvisation. | Sentinel + Phantom | Working product |
| 6 | Deploy | Ship to production. Scan. Verify. | CEO | Live product |
| 7 | Evolve | Health reviews, defense, iteration | Argus (biweekly) | Ongoing health |

## Phase Details

### Phase 1: Research
- **Who:** Researcher agent + web search
- **Input:** Problem space, sector catalog
- **Output:** `specs/SPEC_TEMPLATE.md` — problem definition, market evidence, competitors
- **Rules:**
  - Find problems backed by evidence (URLs, data), not opinions
  - 3+ competitors must be identified
  - Market size estimated (TAM/SAM/SOM)
  - No solution design — that's Phase 2

### Phase 2: Refine
- **Who:** ALL departments, in parallel
- **Input:** SPEC_TEMPLATE from Phase 1
- **Output:** 6 SPEC_MVP files (Engineering, Q&S, Intelligence, Growth, Governance, Design)
- **Rules:**
  - Every agent asks minimum 10 questions with mandatory web search
  - Engineering defines the SOLUTION (tech stack, architecture, features)
  - Q&S defines security plan and test strategy
  - Intelligence defines positioning and competitive angles
  - Growth defines distribution and content strategy
  - Governance defines business model, costs, and legal review

### Phase 3: Post-Refine
- **Who:** Argus (Auditor)
- **Input:** All 6 SPEC_MVP files
- **Output:** Audit report with GO or KILL verdict
- **Rules:**
  - Check for contradictions between department specs
  - Verify evidence quality (every claim needs a source)
  - Evaluate tech stack justification
  - Verify cost projections are realistic
  - Security plan must cover OWASP Top 10

### Phase 4: CEO Gate
- **Who:** CEO (human)
- **Input:** Audit report + all specs + CEO decision checklist
- **Output:** GO (8-10 YES answers) / NO-GO / DEFER
- **Rules:**
  - NO product advances without CEO approval
  - CEO reviews 10-question checklist
  - Only 1 product in phases 1-6 at a time
  - If CEO doesn't respond in 48h: auto-approve with enhanced QA

### Phase 5: Develop
- **Who:** Builder + Designer agents
- **Input:** Approved SPEC_MVP files
- **Output:** Working product matching specs
- **Rules:**
  - Build from specs. No improvisation.
  - Builder and QA alternate sessions (last_actor tracking)
  - Autonomous builds (auto-approved) get Build+QA every session
  - TypeScript strict mode, 0 errors
  - Auth on every endpoint, RLS on every table

### Phase 6: Deploy
- **Who:** Builder (deploy) + Phantom (security) + Sentinel (verify) + Argus (audit)
- **Input:** Product passing all QA/security checks
- **Output:** Live product at production URL
- **Rules:**
  - Post-deploy security scan must pass
  - All endpoints return 200
  - CEO manual PDF delivered
  - CEO must personally verify before moving to Evolve

### Phase 7: Evolve
- **Who:** All departments, ongoing
- **Cadence:** Continuous with biweekly health reviews
- **Rules:**
  - Health reviews scored: GROWING / STABLE / STAGNANT / DECLINING
  - STAGNANT 2x → evaluate redesign/pivot
  - DECLINING 2x → CEO notified, kill evaluation
  - P0/P1 bugs always take priority over new product development
  - Multiple products can be in Evolve simultaneously

## Pipeline Rules

- **1 product in pipeline** (phases 1-6) at a time
- **N products in Evolve** simultaneously
- **Sprint cycle:** Week A = produce (build/ship). Week B = consolidate (position/distribute/improve)
- Schedules 4-9 (Refine phases) skip in Week B

## Quality Gates

Every phase transition requires passing its quality gate. Define gates in `quality-gates.md`.

Template:
```markdown
## Phase X → Y: [Name] → [Name]
**Gatekeeper:** [Agent or CEO]
- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]
```

## State Tracking

Products track their phase in `products/{name}/STATE.md`:

```yaml
phase: DEVELOP          # Current phase
last_actor: "builder"   # Who worked last (for Build↔QA alternation)
last_updated: 2026-03-31
```

The pipeline is tracked globally in `state/PIPELINE.md`.
