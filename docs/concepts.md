# PA·co Concepts

Understanding how the system works before you customize it.

---

## The mental model

PA·co is a coordination layer, not a code framework. It gives each AI agent:
- A defined role (what it owns, what it doesn't touch)
- A layered context system (identity, state, semantic search, archive)
- A structured product lifecycle (7 phases from research to evolve)
- An emergency stop (HALT system)
- Quality gates at every phase transition

Every agent is just Claude Code with instructions. The "team" emerges from how those instructions coordinate through shared state files.

---

## Agents

An agent is a markdown file in `agents/`. When you tell Claude Code "run as /builder," it reads that file and operates by its rules for the entire session.

### What an agent file contains

```yaml
---
name: "Builder"
department: "engineering"
expected_frequency: "hourly"
tools_allowed: ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
tools_denied: []
---

You are the Builder. Your job is to write code, deploy, and maintain products.

## JURISDICTION
I DO: write code, run migrations, deploy, debug
I DO NOT: write marketing copy, evaluate ideas, monitor production

## PROCESS
1. Read state/HALT.md — am I halted?
2. Read state/PIPELINE.md — which product needs work?
3. Read products/{name}/STATE.md — what's the current progress?
4. Do the work
5. Update STATE.md with progress, remaining work, last_actor
6. Git commit and push

## RULES
- Never commit secrets to git
- Test before deploying
- Always update STATE.md at session end
```

### Key design principle: jurisdiction

Every agent has a clear list of what it does and what it explicitly does NOT do. This prevents two agents from both doing the same work. Jurisdiction is what makes the system work.

### Tool whitelisting

Each agent can declare which tools it is allowed or denied:

```yaml
# Auditor: read-only, cannot modify code it reviews
tools_allowed: ["Read", "Glob", "Grep"]

# Researcher: can search but not modify files
tools_denied: ["Write", "Edit"]
```

This enforces least-privilege access and maps directly to the Anthropic Subagents API's per-agent tool restrictions. See [agent-schema.md](../core/agent-schema.md) for the full schema.

### Agent types by frequency

| Type | Frequency | Example |
|------|-----------|---------|
| Core operational | Hourly | Builder (build sessions), QA (review sessions) |
| Regular cadence | Daily | Standup, research, competitive defense |
| On-demand | When needed | Post-refine auditor, CEO gate review |
| Weekly | Once per week | Weekly report, open source sync |

---

## The 7-Phase Workflow

Every product goes through the full lifecycle. No shortcuts, no skipped phases.

```
RESEARCH → REFINE → POST-REFINE → CEO GATE → DEVELOP → DEPLOY → EVOLVE
```

| Phase | What happens | Gatekeeper |
|-------|-------------|------------|
| **Research** | Find problems worth solving. Scan sectors. Output: SPEC_TEMPLATE. | PA·co |
| **Refine** | All departments enrich in parallel. Each asks 10+ questions with web search. Output: 6 spec files. | PA·co |
| **Post-Refine** | Auditor reviews all specs. Fix issues or kill the product. | Auditor |
| **CEO Gate** | Human approves, rejects, or defers. No product advances without CEO approval. | CEO |
| **Develop** | Builder + Designer build from specs. Build/QA alternation enforced. | QA + Security |
| **Deploy** | Ship to production. Security scan. Health verification. | CEO |
| **Evolve** | Continuous improvement: health reviews, competitive defense, feature iteration. | Auditor (periodic) |

**Key constraint:** Only 1 product in phases 1-6 at a time. Multiple products can be in Evolve simultaneously.

See the [7-Phase Workflow guide](workflow.md) for a complete walkthrough, or [workflow-schema.md](../core/workflow-schema.md) for the technical schema.

---

## 4-Layer Context Engineering

Context Engineering is the core innovation. It solves how each agent gets the right information without exceeding context limits.

| Layer | Name | What it provides | Source | Lifecycle |
|-------|------|-----------------|--------|-----------|
| 1 | **Identity** | CLAUDE.md + agent definition + catalogs | Repo files | Read-only per session |
| 2 | **State** | Product STATE.md + PIPELINE.md + HALT.md | `state/`, `products/*/` | Rewritten every session |
| 3 | **Relevant** | Semantic search results from vector DB | pgvector (Supabase) | ~5-10 results per query |
| 4 | **Archive** | Everything in vector DB not returned | Vector database | Grows forever |

**The key insight:** Same agent + different context = different behavior per product. Agent definitions are generic; `products/{name}/` directories make them product-specific.

### Layer 1: Identity (Static)

Loaded at every session start. Defines WHO the agent is.

- `CLAUDE.md` — Organization rules, structure, schedules (max 150 lines)
- `agents/{role}.md` — Mission, jurisdiction, process, rules
- `catalogs/*.md` — Reference material (sectors, tech stacks, business models)

### Layer 2: State (Dynamic)

Current state of work. Rewritten each session — never accumulated.

- `state/PIPELINE.md` — All products and their current phases
- `state/HALT.md` — Emergency stop register
- `state/CEO_BLOCKERS.md` — Items requiring human decision
- `products/{name}/STATE.md` — Progress, bugs, last_actor, metrics

### Layer 3: Relevant (Semantic Search)

Retrieved per session based on the task. Powered by pgvector or similar.

A context assembler generates search queries from the current task, searches the vector DB filtered by department and product, and returns the most relevant entries: lessons learned, competitive intel, design decisions, security findings.

### Layer 4: Archive (Everything Else)

All historical knowledge lives in the vector DB. It grows forever. Agents never see it unless Layer 3 retrieves it. Old STATE.md content, completed project details, and past lessons all live here.

See [context-engineering.md](../core/context-engineering.md) for the full specification, and [templates/context-engineering/](../templates/context-engineering/) for a ready-to-use pgvector setup.

---

## State Management

Products track their own state. A global pipeline tracks all products.

### Directory structure

```
state/
  PIPELINE.md        — All products and their current phase
  HALT.md            — Emergency stop system
  CEO_BLOCKERS.md    — Items requiring human decision

products/{name}/
  CLAUDE.md          — Product-specific rules and stack
  STATE.md           — Progress, bugs, last_actor, metrics
  DISPATCH.md        — Product task queue and handoffs
  BRANDING.md        — Visual identity
  mvp-specs/         — What to build (from Refine phase)
```

### STATE.md — per-product progress

Each product has its own STATE.md that tracks current progress:

```markdown
# ProductName — State

## Current Phase
- phase: DEVELOP
- last_actor: "builder"
- last_updated: 2026-04-05

## Status
- progress: Built auth flow and dashboard. 12 routes.
- remaining: Stripe integration, email notifications.
- bugs_active: 0
- blockers: none
```

**The `last_actor` field** drives Build/QA alternation: if the last actor was "builder", QA runs next. If it was "qa", Builder runs next. This guarantees every build session is followed by a quality check.

### PIPELINE.md — global product tracker

Tracks all products across phases. Enforces the constraint that only 1 product can be in active development (phases 1-6) while multiple products evolve simultaneously.

### Size limits are not optional

State files have hard line limits (STATE: 40 lines, DISPATCH: 100 lines, PIPELINE: 30 lines). When content exceeds limits, archive completed items to the vector DB and rewrite with only current content. This prevents context bloat.

See [state-schema.md](../core/state-schema.md) for the full schema.

---

## The HALT System

HALT is how you stop agents when something goes wrong.

### When to use it

- Security issue that needs your review before agents continue
- Legal concern requiring your input
- Agent went off the rails and you need to course-correct
- You want to pause work while you change strategy

### How it works

Every schedule and agent reads `state/HALT.md` **before doing anything**. If their product or "ALL" is halted, they exit immediately.

```markdown
# state/HALT.md
## Current: CLEAR
No active halts.

## Active Halts:
(none)
```

To halt: write `HALT [product]` or `HALT ALL` in HALT.md, or tell Claude Code:
```
Halt the engineering department. Reason: reviewing security finding.
```

To resume: write `RESUME [product]` or `RESUME ALL`.

Only you (the CEO/operator) can halt or resume. Agents cannot halt each other.

---

## Quality Gates

Quality gates are mandatory checks at every phase transition.

### When gates run

- **Phase 3 (Post-Refine):** Auditor reviews all specs before CEO Gate
- **Phase 5 (Develop):** QA/Security reviews after every build session (Build/QA alternation)
- **Phase 6 (Deploy):** Security scan + health check before going live
- **Phase 7 (Evolve):** Periodic audits of live products

### What gets checked

The auditor reads quality gate checklists defined per output type:

- **Code:** TypeScript strict mode, no secrets in code, RLS on every table, auth on every endpoint
- **Research:** Claims backed by URLs and data, 3+ competitors identified, market size estimated
- **Specs:** Measurable milestones, cost model included, security plan covers OWASP Top 10
- **Deploys:** All endpoints return 200, security headers present, monitoring configured

A BLOCKER finding means the phase transition is paused until resolved.

See [workflow-schema.md](../core/workflow-schema.md) for phase transition rules and gate definitions.

---

## The Orchestrator (PA·co)

The orchestrator (`agents/paco.md`) is the master coordinator. It doesn't do the work — it ensures the work gets done.

**What it does:**
- Runs the daily standup (reads all state files, checks agent health)
- Routes cross-department handoffs via DISPATCH.md files
- Identifies blockers and escalates to `state/CEO_BLOCKERS.md`
- Manages the HALT system
- Triggers phase transitions when gates are passed

**What it doesn't do:**
- Write code (that's Builder)
- Create content (that's Marketer)
- Run security scans (that's Security)

The orchestrator is the team lead, not the doer.

---

## How it all fits together

A typical day in a PA·co system with a product in the Develop phase:

```
8:00 AM  — Standup reads state/PIPELINE.md, all STATE.md files, CEO_BLOCKERS.md.
            Reports: "ProductX in DEVELOP, last_actor=qa. Builder's turn."

9:00 AM  — Builder session starts.
            Reads HALT.md (CLEAR).
            Reads products/productx/STATE.md (last_actor=qa → my turn).
            Reads products/productx/mvp-specs/ for what to build.
            Searches pgvector for relevant lessons.
            Builds the next feature.
            Updates STATE.md: last_actor="builder", progress logged.
            Git commit and push.

10:00 AM — QA session starts.
            Reads STATE.md (last_actor=builder → my turn).
            Reviews the code changes.
            Runs security checks.
            Updates STATE.md: last_actor="qa", qa_result logged.
            If bugs found: logs them in STATE.md for Builder.

11:00 AM — Builder session starts.
            Reads STATE.md (last_actor=qa → my turn).
            Fixes any bugs from QA, continues building.
            Cycle repeats hourly.

2:00 PM  — Competitive Defense scans competitors for products in Evolve.
            Adds new threats or opportunities to pending_work in STATE.md.

5:00 PM  — Weekly report summarizes the week for the CEO.
```

No agent talks to another directly. State files are the shared context. The 7-phase workflow provides the structure. Build/QA alternation ensures quality.

---

Next: [Architecture](architecture.md) — technical system design | [A2A Protocol](a2a-protocol.md) — how agents coordinate work | [Subagents API](subagents.md) — spawn agents via the Claude Agent SDK | [MCP Transports](mcp-transports.md) — connect to external tools | [Adding Agents](adding-agents.md) — create custom agents for your needs.
