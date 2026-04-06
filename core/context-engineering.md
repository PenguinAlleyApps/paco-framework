# PA·co Context Engineering — 4 Layers

> Every agent session is shaped by the context it receives. This schema defines how context flows through the system.

## The 4 Layers

| Layer | Name | What | Lifecycle | Size Limit |
|-------|------|------|-----------|------------|
| 1 | **Identity** | CLAUDE.md + agent.md + catalogs | Read-only per session | CLAUDE.md: 150 lines |
| 2 | **State** | STATE.md + DISPATCH_TODAY + PIPELINE | Rewritten every session | STATE.md: 40 lines |
| 3 | **Relevant** | Semantic search results (pgvector or similar) | Assembled per session (~5-10 results) | Auto-selected |
| 4 | **Archive** | Everything in vector DB not returned | Grows forever, never deleted | Unlimited |

## Layer 1: Identity (Static)

Loaded at the start of every session. Defines WHO the agent is.

```
CLAUDE.md              — Organization rules, structure, schedules
agents/{role}.md       — Agent definition (mission, jurisdiction, process)
catalogs/*.md          — Reference catalogs (sectors, tech stacks, etc.)
```

**Rule:** CLAUDE.md max 150 lines. If it exceeds 145, restructure automatically.

## Layer 2: State (Dynamic, Rewritten)

Current state of work. Rewritten each session — never accumulated.

```
state/PIPELINE.md      — All products and their current phases
state/DISPATCH_TODAY.md — Today's task assignments and priorities
state/HALT.md          — Emergency stop register
state/CEO_BLOCKERS.md  — Items requiring CEO decision
products/{name}/STATE.md — Per-product progress, bugs, metrics
```

**Rules:**
- STATE.md: REWRITE every session. Only current state, never history.
- DISPATCH_TODAY: REWRITE daily. Yesterday's dispatch is gone.
- PIPELINE: Only active items. Completed products archived to vector DB.

## Layer 3: Relevant (Semantic Search)

Retrieved per session based on the task at hand. Powered by vector search (pgvector, Pinecone, or similar).

**How it works:**
1. Context assembler receives: agent_role, product_name, task_description
2. Generates 2-3 search queries from task_description
3. Searches vector DB filtered by department + product
4. Returns ~5-10 most relevant entries

**What gets stored in the vector DB:**
- Lessons learned (with WHEN/THEN/NEVER/BECAUSE format)
- Market intelligence and competitive analysis
- Design decisions and their reasoning
- Security findings and audit results

### Knowledge Entry Format (Recommended)
```
WHEN: [trigger situation]
THEN: [correct action]
NEVER: [prohibited action]
BECAUSE: [why — the incident or evidence]
VERIFY: [how to check compliance]
SOURCE: [date, agent, product]
```

### Metadata Schema
```json
{
  "type": "lesson|market_intel|competitive_intel|design_system|security|decision",
  "scope": "universal|product_specific",
  "product": "product-name|null",
  "department": "engineering|quality-security|intelligence|growth|governance|executive",
  "tags": ["relevant", "tags"],
  "source": "standup|session|research|audit",
  "date": "YYYY-MM-DD"
}
```

## Layer 4: Archive (Everything Else)

All vector DB entries not returned by Layer 3 search. Never deleted. Grows forever. Available if search queries change.

## Size Limits (Enforced)

| File | Max Lines | Action When Exceeded |
|------|-----------|---------------------|
| CLAUDE.md (root) | 150 | Move detail to playbooks/ or catalogs/ |
| products/{name}/CLAUDE.md | 80 | Move detail to product's specs/ |
| products/{name}/STATE.md | 40 | Archive old milestones to vector DB |
| state/DISPATCH_TODAY.md | 50 | Resets daily |
| state/PIPELINE.md | 30 | Only active products |
| Agent files (agents/*.md) | 50 | Move detail to playbooks/ |

## Without a Vector DB

If you don't have pgvector or similar set up, Layers 3-4 fall back to file-based memory:

```
memory/
  MEMORY.md              — Index (max 80 lines)
  lessons-learned.md     — Institutional memory (max 50 active)
  decisions/             — Decision logs
  market-intel/          — Research findings
```

This works for small teams. As knowledge grows past ~100 entries, migrate to a vector DB for better retrieval. See [templates/context-engineering/](../templates/context-engineering/) for a complete pgvector setup guide with SQL schema, ingestion, and search scripts.

## Rewrite vs Accumulate

| File | Strategy | Why |
|------|----------|-----|
| STATE.md | Rewrite | Only current state matters |
| DISPATCH_TODAY.md | Rewrite daily | Yesterday's tasks are history |
| PIPELINE.md | Rewrite | Only active products |
| Vector DB | Accumulate forever | Historical knowledge has value |
| lessons-learned.md | Accumulate, then graduate | Move to vector DB when codified |
