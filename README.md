# PA·co Framework

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Claude Code](https://img.shields.io/badge/Claude_Code-Required-blue.svg)
![Status](https://img.shields.io/badge/Status-v2.0-brightgreen.svg)
![Agents](https://img.shields.io/badge/Agents-3_to_16+-purple.svg)

**The markdown-first, zero-code multi-agent operations system for Claude Code.**

Turn your Claude Code instance into an autonomous team of AI agents that coordinate, learn, and evolve — without writing a single line of Python.

```
                         ┌─────────────┐
                         │     CEO     │
                         │  (You)      │
                         └──────┬──────┘
                                │ halt / resume / approve
                         ┌──────▼──────┐
                         │   PA·co     │
                         │ Orchestrator│ ← 4-layer context
                         └──────┬──────┘
                 ┌──────────────┼──────────────┐
                 │              │              │
          ┌──────▼──────┐ ┌────▼────┐ ┌───────▼──────┐
          │ Engineering │ │  Q & S  │ │ Intelligence │ ...
          │             │ │         │ │              │
          │ Builder     │ │ QA      │ │ Researcher   │
          │ Designer    │ │ Auditor │ │ Strategist   │
          └──────┬──────┘ └────┬────┘ └───────┬──────┘
                 │              │              │
          products/        state/          catalogs/
          {name}/STATE     PIPELINE.md     sectors.md
                           HALT.md         tech-stacks.md
                 └──────────────┼──────────────┘
                                │
                    ┌───────────▼───────────┐
                    │  Context Engineering  │
                    │  4 Layers: Identity → │
                    │  State → Relevant →   │
                    │  Archive (pgvector)   │
                    └──────────────────────┘
```

---

## What is PA·co?

PA·co (Penguin Alley Commander/Officer) is a framework for building multi-agent AI systems using only markdown files. Define agents, set up coordination, and let Claude Code run your operations autonomously.

**No code. No databases required. Just markdown.**

```
You get:
- 3-16 specialized AI agents with clear roles
- A 7-phase product workflow (Research → Evolve)
- 4-layer Context Engineering for perfect agent memory
- Quality gates that catch mistakes before you see them
- An emergency halt system so you stay in control
- Scheduled tasks for 24/7 autonomous operations
- Optional: pgvector for semantic knowledge retrieval
```

## Why PA·co?

| Problem | PA·co Solution |
|---------|---------------|
| AI agents step on each other's work | **State management** — product-centric coordination with Build↔QA alternation |
| Agents repeat the same mistakes | **4-layer Context Engineering** — knowledge persists and surfaces when relevant |
| Can't stop agents when things go wrong | **HALT system** — pause any product or all operations instantly |
| No quality control on agent output | **Quality gates** — every phase transition has mandatory checks |
| No structure for going from idea to shipped product | **7-phase workflow** — Research → Refine → Post-Refine → CEO Gate → Develop → Deploy → Evolve |
| Setup requires Python/code expertise | **Zero code** — everything is markdown files |

## Quick Start

1. Clone this repo into your project
2. Run the bootstrap prompt in Claude Code:
   ```
   Read paco-bootstrap.md and execute the setup
   ```
3. Answer 5-7 questions about your project
4. PA·co generates your entire multi-agent system
5. Run your first standup: "Run as /paco — execute daily standup"

## Architecture: v2

### 7-Phase Workflow

Every product goes through the full workflow. No shortcuts.

```
RESEARCH → REFINE → POST-REFINE → CEO GATE → DEVELOP → DEPLOY → EVOLVE
```

| Phase | Purpose | Gatekeeper |
|-------|---------|------------|
| Research | Find problems, not solutions | PA·co |
| Refine | All departments enrich in parallel | PA·co |
| Post-Refine | Audit specs. Fix or kill. | Auditor |
| CEO Gate | Human approval required | CEO |
| Develop | Build from specs. No improvisation. | QA + Security |
| Deploy | Ship, scan, verify | CEO |
| Evolve | Health reviews, iteration, defense | Auditor (biweekly) |

See [core/workflow-schema.md](core/workflow-schema.md) for full details.

### 4-Layer Context Engineering

Every agent session receives precisely the context it needs:

| Layer | What | Example |
|-------|------|---------|
| **Identity** | CLAUDE.md + agent definition + catalogs | "You are the Builder. Here are org rules." |
| **State** | Product STATE.md + Pipeline + Today's dispatch | "Product X is in Develop. QA passed. Your turn." |
| **Relevant** | Semantic search from vector DB | "Last time we deployed, CSP headers were missing." |
| **Archive** | Everything else in vector DB | Available if search queries change |

See [core/context-engineering.md](core/context-engineering.md) for full details.

### State Management

Products track their own state. A global pipeline tracks all products.

```
state/
  PIPELINE.md        — All products and phases
  HALT.md            — Emergency stop
  CEO_BLOCKERS.md    — Items needing CEO decision
  DISPATCH_TODAY.md  — Today's assignments

products/{name}/
  CLAUDE.md          — Product-specific rules
  STATE.md           — Progress, bugs, metrics
  mvp-specs/         — What to build
```

See [core/state-schema.md](core/state-schema.md) for full details.

### Agents

Each agent is a markdown file that defines a role:

```yaml
---
name: "Builder"
department: "engineering"
expected_frequency: "hourly"
---

You are the Builder. Your job is to write code, deploy, and maintain products.

## I DO:
- Write code, run migrations, deploy

## I DO NOT:
- Create marketing content (that's /marketer)
```

See [core/agent-schema.md](core/agent-schema.md) for the full schema.

### Scheduling

Agents run on schedules via Claude Code scheduled tasks or hooks:

| Type | Example |
|------|---------|
| Jornada (work hours) | Standup 8am, Refine phases 8:30-10:30am |
| 24/7 Automation | Build sessions hourly, QA alternating, email relay |
| Weekly | Friday reports, open source sync |

### Emergency Halt

```markdown
# state/HALT.md
## Current: CLEAR
```

Write "HALT [product]" or "HALT ALL" to stop operations. Only the CEO can halt/resume.

## Templates

### Free Templates (included in repo)

| Template | Agents | Best for |
|----------|--------|----------|
| `solo-founder` | 4 (orchestrator, builder, devops, marketer) | Solo builders shipping fast |
| `startup` | 8 (adds QA, researcher, strategist, sales) | Small teams with product-market fit goals |

### Premium Templates

Industry-specific templates with specialized agents, workflows, and dispatch patterns.

| Template | Agents | Price | Get it |
|----------|--------|-------|--------|
| **Agency** | 6 (multi-client coordination) | $99 | [Buy on Gumroad](https://penguinmaster06.gumroad.com/l/rjihs) |
| **E-Commerce** | 6 (inventory, support, analytics) | $79 | [Buy on Gumroad](https://penguinmaster06.gumroad.com/l/jvsfza) |
| **Content Studio** | 5 (writer, editor, SEO, social) | $49 | [Buy on Gumroad](https://penguinmaster06.gumroad.com/l/ffpnl) |
| **Dev Team** | 6 (code review, QA, security, DevOps) | $79 | [Buy on Gumroad](https://penguinmaster06.gumroad.com/l/mexvb) |
| **Complete Bundle** | All 4 + future templates | $249 | [Buy on Gumroad](https://penguinmaster06.gumroad.com/l/weome) |

## Comparison

| Feature | PA·co v2 | CrewAI | LangGraph | AutoGen |
|---------|----------|--------|-----------|---------|
| Language needed | None (markdown) | Python | Python | Python |
| Setup time | 5 minutes | Hours | Hours | Hours |
| Product lifecycle | 7-phase workflow | None | None | None |
| Context management | 4-layer engineering | In-memory/DB | State machine | Messages |
| Quality gates | Built-in per phase | None | None | None |
| Emergency halt | Built-in | None | None | None |
| Knowledge persistence | Vector DB + files | RAG (optional) | None | None |
| CEO approval gates | Built-in | None | None | None |
| Cost | $0 extra | API costs | API costs | API costs |

## Battle-Tested

PA·co isn't theoretical. We built and operate [Penguin Alley](https://penguinalley.com) entirely with PA·co:

- **12 agents** across 5 departments + Executive
- **7-phase workflow** running autonomously 24/7
- **19 scheduled tasks** covering research, build, QA, distribution, and more
- **4-layer Context Engineering** with pgvector semantic search
- **Multiple products** shipped through the full pipeline
- **$0 infrastructure cost** — all free tiers

Every pattern in this framework comes from real production experience.

## Core Schemas

| Schema | What it defines |
|--------|----------------|
| [agent-schema.md](core/agent-schema.md) | Agent file structure and design principles |
| [context-engineering.md](core/context-engineering.md) | 4-layer context system |
| [workflow-schema.md](core/workflow-schema.md) | 7-phase product workflow |
| [state-schema.md](core/state-schema.md) | Product state and pipeline tracking |
| [dispatch-schema.md](core/dispatch-schema.md) | v1 dispatch system (still works for simple setups) |
| [memory-schema.md](core/memory-schema.md) | File-based memory (v1, fallback for no vector DB) |
| [executive-orders-template.md](core/executive-orders-template.md) | CEO directives template |

## Documentation

- [Getting Started](docs/getting-started.md) — Full setup guide
- [Concepts](docs/concepts.md) — How departments, context, and workflows work
- [Adding Agents](docs/adding-agents.md) — Create custom agents for your needs
- [FAQ](docs/faq.md) — Common questions

## Requirements

- **Claude Code** (CLI, Desktop app, VS Code extension, or JetBrains extension)
- **Claude Pro/Max** for scheduled tasks (optional — can run agents manually)
- Any project type: SaaS, agency, content, dev tools, research, etc.

## License

MIT — use it however you want.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome:
- New agent templates
- New department configurations
- Industry-specific templates
- Documentation improvements
- Bug reports and feature requests

---

**Built by [PA·co](https://penguinalley.com) — A Penguin Alley System**
