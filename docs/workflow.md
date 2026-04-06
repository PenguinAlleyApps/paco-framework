# The 7-Phase Workflow

Every product goes through the same lifecycle. No shortcuts, no tiers.

```
RESEARCH → REFINE → POST-REFINE → CEO GATE → DEVELOP → DEPLOY → EVOLVE
```

---

## Why 7 phases?

Most teams skip straight from "idea" to "build." PA·co forces a research-first approach because building the wrong thing is the most expensive mistake a small team can make.

Each phase has a gatekeeper — either an agent or you (the CEO/operator). Nothing moves forward without passing its gate.

---

## Phase 1: Research

**Goal:** Find a real problem backed by evidence.

**Who runs it:** Researcher agent + web search

**What happens:**
1. Agent scans the sector catalog for problem areas
2. Searches the web for evidence: pain points, competitor gaps, market data
3. Identifies 3+ existing solutions and their weaknesses
4. Estimates market size (TAM/SAM/SOM)
5. Produces a `specs/SPEC_TEMPLATE.md`

**Key rule:** Research finds PROBLEMS, not solutions. No tech stack decisions, no feature lists. Just evidence that a real problem exists for real people.

**Output:**
```
specs/SPEC_TEMPLATE.md
├── Problem definition (with evidence URLs)
├── Target user profile
├── Competitor analysis (3+ competitors)
├── Market size estimate
└── Pain level assessment (1-10)
```

**Gate:** PA·co reviews the SPEC_TEMPLATE. Is the problem real? Is the evidence solid?

---

## Phase 2: Refine

**Goal:** Every department enriches the spec in parallel.

**Who runs it:** All departments simultaneously

**What happens:**
1. Engineering defines the technical solution (stack, architecture, MVP scope)
2. Quality & Security defines the security plan and test strategy
3. Intelligence & Strategy defines positioning and competitive angles
4. Growth & Revenue defines distribution and content strategy
5. Governance defines the business model, costs, and legal requirements

**Key rule:** Every agent asks minimum 10 questions with mandatory web search before writing its spec. No assumptions — verify everything.

**Output:** 6 SPEC_MVP files, one per department:
```
specs/
├── SPEC_MVP_ENGINEERING.md
├── SPEC_MVP_QUALITY_SECURITY.md
├── SPEC_MVP_INTELLIGENCE.md
├── SPEC_MVP_GROWTH.md
├── SPEC_MVP_GOVERNANCE.md
└── SPEC_MVP_DESIGN.md
```

**Gate:** All 6 specs complete and internally consistent.

---

## Phase 3: Post-Refine

**Goal:** Independent audit of all specs before CEO review.

**Who runs it:** Auditor agent (Argus)

**What happens:**
1. Reads all 6 SPEC_MVP files
2. Checks for contradictions between departments
3. Verifies evidence quality (every claim needs a source)
4. Evaluates tech stack justification
5. Checks cost projections against business model
6. Verifies security plan covers OWASP Top 10

**Output:** Audit report with verdict: **GO** or **KILL**

A KILL verdict means the product has a fundamental problem — contradictions between specs, unsupported claims, or unrealistic projections. The team fixes the issues and re-submits, or the product is abandoned.

**Gate:** Argus signs off with GO.

---

## Phase 4: CEO Gate

**Goal:** Human decision. You decide if this product gets built.

**Who runs it:** You (the CEO/operator)

**Input:** Audit report + all specs + a 10-question decision checklist

**The checklist:**
1. Is the problem real and validated?
2. Is the target user clearly defined?
3. Is the competitive advantage defensible?
4. Is the tech stack justified?
5. Is the business model viable?
6. Are costs realistic for your resources?
7. Does the security plan cover the basics?
8. Is the distribution strategy concrete?
9. Can this ship in the projected timeline?
10. Does this align with your mission?

**Decisions:** GO (8+ YES) / NO-GO / DEFER

**Key rules:**
- Only 1 product in phases 1-6 at a time
- Products in Evolve don't count against this limit
- If you don't respond in 48 hours, PA·co auto-approves with enhanced QA

**Gate:** Your explicit approval.

---

## Phase 5: Develop

**Goal:** Build exactly what the specs describe.

**Who runs it:** Builder + Designer agents

**What happens:**
1. Builder reads the approved specs and current STATE.md
2. Builds the next piece of the MVP
3. Updates STATE.md with progress and sets `last_actor: "builder"`
4. QA/Security agent runs next session (Build/QA alternation)
5. QA verifies the build, reports bugs, sets `last_actor: "qa"`
6. Builder fixes bugs next session
7. Cycle continues until all spec items are complete

**Build/QA alternation** is the core pattern:
```
Builder → QA → Builder → QA → Builder → QA → Done
```

The `last_actor` field in STATE.md controls whose turn it is. Builder never runs twice in a row. QA never runs twice in a row. This prevents drift and catches issues early.

**Key rules:**
- Build from specs. No improvisation.
- TypeScript strict mode, 0 errors
- Auth on every endpoint, RLS on every table
- When MVP is complete: set `phase: "READY_FOR_FINAL_QA"`

**Gate:** All spec items built and QA-verified with 0 bugs.

---

## Phase 6: Deploy

**Goal:** Ship to production safely.

**Who runs it:** Builder (deploy) + Phantom (security scan) + Sentinel (verify) + Argus (audit)

**What happens:**
1. Builder deploys to production (Vercel, Cloudflare, or target platform)
2. Phantom runs post-deploy security scan
3. Sentinel verifies all endpoints return 200
4. Argus runs post-deploy audit
5. If all pass: status becomes `DEPLOYED_PENDING_CEO`
6. You verify the live product personally

**Key rules:**
- Security scan must pass before the product is considered live
- You must personally verify before moving to Evolve
- If any check fails: product returns to Develop for fixes

**Gate:** Your personal verification of the live product.

---

## Phase 7: Evolve

**Goal:** Keep the product healthy and competitive.

**Who runs it:** All departments, ongoing

**What happens:**
- Competitive defense: monitoring competitors for new features and threats
- Bug fixes: P0/P1 bugs always take priority over new product development
- Feature iteration: planned improvements based on user feedback and market shifts
- Health reviews: scored GROWING / STABLE / STAGNANT / DECLINING

**Health scoring:**
| Score | Meaning | Action |
|-------|---------|--------|
| GROWING | Metrics improving | Continue current strategy |
| STABLE | Metrics flat | Identify growth opportunities |
| STAGNANT (2x) | No growth for 2 review periods | Evaluate redesign or pivot |
| DECLINING (2x) | Metrics dropping for 2 periods | CEO notified, kill evaluation |

**Key rules:**
- Multiple products can be in Evolve simultaneously
- P0/P1 bugs in any Evolve product take priority over new product development
- Week A (Sprint) focuses on building; Week B (Consolidation) focuses on distribution and improvement

---

## Pipeline tracking

The pipeline is tracked in two places:

**Global:** `state/PIPELINE.md` — all products and their current phase
**Per-product:** `products/{name}/STATE.md` — detailed progress, bugs, last_actor

```yaml
# products/my-app/STATE.md
phase: DEVELOP
last_actor: "qa"
last_updated: 2026-04-01

progress: Auth + dashboard built. 2 bugs fixed.
remaining: Payments integration, deploy prep.
bugs_active: 0
```

---

## Customizing the workflow

The 7 phases are the core framework, but you can adjust:

- **Skip Refine departments** you don't have (e.g., solo founders may skip Governance)
- **Adjust the CEO Gate checklist** to match your priorities
- **Change health review frequency** (default: biweekly in Evolve)
- **Modify quality gate checklists** for your tech stack

What you should NOT change:
- The phase order (Research before Build is non-negotiable)
- The CEO Gate requirement (human oversight is the safety net)
- Build/QA alternation (this catches issues that single-pass development misses)

---

## Quick reference

| Phase | Duration | Who | Output |
|-------|----------|-----|--------|
| Research | 1-2 days | Researcher | SPEC_TEMPLATE |
| Refine | 1 day | All departments | 6 SPEC_MVP files |
| Post-Refine | Hours | Auditor | GO/KILL verdict |
| CEO Gate | Up to 48h | You | GO/NO-GO/DEFER |
| Develop | Days-weeks | Builder + QA | Working product |
| Deploy | Hours | Builder + Security | Live product |
| Evolve | Ongoing | All | Continuous health |

---

Next: [Architecture](architecture.md) — how the system is designed internally.
