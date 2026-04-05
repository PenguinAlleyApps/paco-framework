# PA·co Architecture

Technical architecture of the PA·co multi-agent operating system for Claude Code.

---

## System overview

PA·co Framework is a file-based orchestration layer that transforms Claude Code into an autonomous multi-agent system. There is no runtime server, no message broker, no custom SDK. Agents coordinate through shared markdown files that Claude Code reads and writes during each session.

```
+--------------------------------------------------------------------+
|                        CLAUDE CODE RUNTIME                          |
|                                                                     |
|  +-----------+    +-----------+    +-----------+    +-----------+   |
|  | Session 1 |    | Session 2 |    | Session 3 |    | Session N |   |
|  | (Builder) |    |   (QA)    |    |(Researcher)|   | (Marketer)|   |
|  +-----+-----+    +-----+-----+    +-----+-----+    +-----+-----+  |
|        |                |                |                |         |
|  +-----v----------------v----------------v----------------v-----+   |
|  |                   FILE SYSTEM (shared state)                 |   |
|  |                                                              |   |
|  |  CLAUDE.md          state/PIPELINE.md    products/{name}/    |   |
|  |  agents/{role}.md   state/HALT.md        STATE.md            |   |
|  |  catalogs/*.md      state/CEO_BLOCKERS   DISPATCH.md         |   |
|  +------------------------------+-------------------------------+   |
|                                 |                                   |
|  +------------------------------v-------------------------------+   |
|  |                     PGVECTOR (archive)                       |   |
|  |  Lessons, decisions, competitive intel, research results     |   |
|  +--------------------------------------------------------------+   |
+--------------------------------------------------------------------+
```

Every session is independent. Agents never share runtime memory. Coordination happens exclusively through file reads and writes between sessions.

---

## Core architectural decisions

### Why files instead of message passing

Traditional multi-agent frameworks (CrewAI, LangGraph, AutoGen) coordinate agents via in-memory message passing or runtime APIs. PA·co uses the file system instead:

| Decision | Rationale |
|----------|-----------|
| Markdown files for state | Claude Code natively reads and writes files. No serialization, no adapters, no custom protocol. |
| No runtime server | Eliminates infrastructure cost, deployment complexity, and single points of failure. |
| Session isolation | Each agent session starts clean. No leaked state, no memory corruption, no context pollution across agents. |
| Human-readable state | Anyone can inspect, debug, or manually override the system by editing a markdown file. |

### Why single-agent sessions

PA·co does not run multiple agents simultaneously in a single session. Each Claude Code session loads exactly one agent identity. This eliminates:

- Context window competition between agents
- Role confusion (Claude trying to act as multiple agents at once)
- Unpredictable execution order within a session

The trade-off is latency: agent coordination happens across sessions (minutes) rather than within a session (seconds). For product development workflows, this latency is acceptable and the reliability gain is significant.

---

## The four-layer context system

Every agent session assembles its context from four layers. This is the core architectural innovation of PA·co.

```
Layer 1: IDENTITY (always loaded)
  CLAUDE.md ──> System rules, org structure, workflow, schedules
  agents/{role}.md ──> Agent mission, jurisdiction, tools, rules
  catalogs/*.md ──> Domain knowledge (sectors, tech stacks, business models)

Layer 2: STATE (rewritten each session)
  state/PIPELINE.md ──> All products and their current phase
  state/HALT.md ──> Emergency stop status
  products/{name}/STATE.md ──> Product progress, bugs, last_actor
  products/{name}/DISPATCH.md ──> Cross-department handoffs

Layer 3: RELEVANT (queried per session)
  pgvector search ──> 5-10 semantically relevant results
  Source: lessons, decisions, competitive intel, research

Layer 4: ARCHIVE (never loaded directly)
  Everything in pgvector not returned by Layer 3
  Grows indefinitely. Available via semantic search.
```

### Why four layers matter

Without layered context, multi-agent systems face two failure modes:

1. **Context starvation** -- The agent lacks critical information and makes incorrect decisions.
2. **Context flooding** -- The agent receives too much information, exceeds token limits, and loses focus.

PA·co solves both by ensuring each layer serves a distinct purpose with a distinct lifecycle:

| Layer | Size budget | Refresh rate | Failure if missing |
|-------|------------|-------------|-------------------|
| Identity | ~3,000 tokens | Once per session | Agent has no role or rules |
| State | ~1,500 tokens | Every session | Agent repeats completed work |
| Relevant | ~500-1,000 tokens | Per query | Agent lacks lessons from past mistakes |
| Archive | Unlimited | Never loaded | No immediate failure (searchable on demand) |

### File size enforcement

No file exceeds 150 lines or 10KB. This is enforced by a Size Guard that runs in build sessions. When a file approaches the limit:

1. Historical content is extracted into timestamped lesson files
2. The file is rewritten with only current/active content
3. Extracted lessons are ingested into pgvector (Layer 4)

This prevents the unbounded file growth that caused context window exhaustion in PA·co v1.

---

## Agent architecture

### Agent definition structure

Each agent is a markdown file with YAML frontmatter:

```yaml
---
name: "Builder"
department: "engineering"
model: "sonnet"
expected_frequency: "hourly"
tools_allowed: ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
---

## MISSION
Build products from specifications. Ship working code.

## JURISDICTION
I DO: write code, run migrations, deploy, debug
I DO NOT: write marketing copy, evaluate ideas, approve spending

## PROCESS
1. Check HALT.md
2. Check PIPELINE.md for products in DEVELOP
3. Read product STATE.md -- is it my turn? (last_actor != "builder")
4. Read product specs in mvp-specs/
5. Build the next piece
6. Update STATE.md: last_actor = "builder"
7. Git commit + push
```

### Department organization

Agents are grouped into departments. Each department has clear boundaries:

```
Executive
  PA·co (COO) ── Orchestrates all agents, maintains system health

Engineering
  Builder ── Writes code, deploys, maintains products
  Designer ── Creates UI/UX, design systems, visual assets

Quality & Security
  QA ── Tests every build, verifies deployments
  Security ── Scans for vulnerabilities, enforces security policies
  Auditor ── Reviews phase transitions, audits specs

Intelligence & Strategy
  Researcher ── Finds problems, scans markets, tracks trends
  Strategist ── Analyzes competition, identifies opportunities

Growth & Revenue
  Marketer ── Creates content, manages brand, runs campaigns
  Sales ── Generates leads, manages partnerships, outreach
```

### Build/QA alternation

The `last_actor` field in each product's STATE.md enforces strict alternation between building and quality assurance:

```
Builder runs ──> sets last_actor = "builder"
  Next hourly session: QA runs (last_actor is "builder", so QA's turn)
QA runs ──> sets last_actor = "qa"
  Next hourly session: Builder runs (last_actor is "qa", so Builder's turn)
```

This guarantees every code change is reviewed before the next change is made. No build session can run twice in a row without QA verification in between.

---

## Product lifecycle

### The 7-phase workflow

```
RESEARCH ──> REFINE ──> POST-REFINE ──> CEO GATE ──> DEVELOP ──> DEPLOY ──> EVOLVE
   |            |            |              |            |           |          |
   v            v            v              v            v           v          v
 Find the    Enrich      Audit all     Human        Build      Ship to     Iterate,
 problem     spec in     specs.        approves     from       prod.       defend,
 first.      parallel.   Fix or kill.  or kills.    specs.     Verify.     improve.
```

Each phase transition requires passing a quality gate. Gates are defined per-phase and enforced by the Auditor agent.

### Pipeline constraints

- **One product in phases 1-6 at a time.** This prevents context switching and ensures focus.
- **Multiple products in Evolve simultaneously.** Once shipped, products receive continuous maintenance.
- **Sprint/Consolidation cycle.** Week A produces (build/ship). Week B consolidates (distribute/improve).

### State tracking

Global state:

```markdown
# state/PIPELINE.md
| Product   | Phase    | Status           | Last Updated |
|-----------|----------|-----------------|-------------|
| Compliora | EVOLVE_A | Dashboard shipped | 2026-04-05  |
```

Per-product state:

```markdown
# products/compliora/STATE.md
- phase: EVOLVE_A
- last_actor: "builder"
- last_updated: 2026-04-05
- progress: Compliance dashboard built
- remaining: SEO, messaging update
- bugs_active: 0
```

---

## Scheduling system

PA·co uses Claude Code scheduled tasks to run agents autonomously. Schedules are organized into three tiers:

| Tier | When | Examples |
|------|------|---------|
| Work hours (7am-2pm) | Daily, sequential | Standup, Refine phases, Research, Competitive Defense |
| 24/7 automation | Hourly | Build sessions, QA reviews, email relay |
| Weekly | Friday | Reports, open source sync |

### Smart-skip logic

Every schedule checks preconditions before executing. If there is no work to do, the agent exits silently. Examples:

- Build Session: skips if no product in DEVELOP, or if `last_actor = "builder"`
- Refine phases: skip in Week B (consolidation week)
- QA Review: skips if `last_actor = "qa"` (Builder hasn't run yet)

This prevents wasted Claude Code usage and empty output.

---

## Emergency halt system

The HALT system provides instant, global control:

```markdown
# state/HALT.md
## Current: HALT ALL
Reason: Token conservation. Resumes Saturday.
```

Every schedule reads `state/HALT.md` as its first action. If halted, the session exits immediately. Only the human operator can halt or resume. This is the kill switch for the entire system.

Halt scopes: `HALT ALL` stops everything. `HALT [product]` stops only that product's schedules.

---

## Integration points

### pgvector (semantic memory)

PA·co uses Supabase pgvector for long-term memory:

- **Ingestion:** Lessons, decisions, and competitive intel are embedded and stored
- **Retrieval:** Agents query pgvector for relevant context (Layer 3)
- **Types:** `lesson`, `decision`, `competitive_intel`, `research`, `content`
- **Scoping:** Results filtered by product, agent, or department

### Claude Agent SDK (Subagents API)

PA·co agents map directly to the Anthropic Subagents API:

| PA·co concept | SDK equivalent |
|--------------|---------------|
| Agent markdown file | `AgentDefinition` |
| `tools_allowed` | `allowed_tools` |
| Agent session | `agent.run()` |
| Department isolation | Separate agent instances |

See [subagents.md](subagents.md) for full integration guide.

### MCP servers

PA·co agents use MCP (Model Context Protocol) servers for external tool access. Tool access is controlled per-agent via `tools_allowed` and `tools_denied` in the agent definition.

### Scheduled tasks

Claude Code scheduled tasks trigger agent sessions on cron schedules. Each schedule is a prompt file that loads the appropriate agent identity and executes the defined workflow.

---

## Security model

| Control | Implementation |
|---------|---------------|
| Least privilege | Per-agent tool restrictions via `tools_allowed`/`tools_denied` |
| Human oversight | CEO Gate blocks product advancement without human approval |
| Emergency stop | HALT system halts any or all operations instantly |
| Spending control | Zero spending authority. All purchases require human approval. |
| Audit trail | Every session updates STATE.md. Git history provides full audit log. |
| Session isolation | No shared runtime state between agent sessions |

---

## Navigation

- [Getting Started](getting-started.md) -- Setup guide
- [Concepts](concepts.md) -- Mental model and key ideas
- [Adding Agents](adding-agents.md) -- Create custom agents
- [A2A Protocol](a2a-protocol.md) -- Agent coordination patterns
- [Subagents API](subagents.md) -- Claude Agent SDK integration
- [FAQ](faq.md) -- Common questions
- [Comparisons](comparisons.md) -- PA·co vs other frameworks
