# PA·co Framework

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Claude Code](https://img.shields.io/badge/Claude_Code-Required-blue.svg)
![Status](https://img.shields.io/badge/Status-Beta_v0.1-orange.svg)
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
                         │ Orchestrator│ ← reads ALL dispatches
                         └──────┬──────┘
                 ┌──────────────┼──────────────┐
                 │              │              │
          ┌──────▼──────┐ ┌────▼────┐ ┌───────▼──────┐
          │ Engineering │ │  Q & S  │ │ Intelligence │ ...
          │             │ │         │ │              │
          │ Builder     │ │ QA      │ │ Researcher   │
          │ DevOps      │ │ Auditor │ │ Strategist   │
          └──────┬──────┘ └────┬────┘ └───────┬──────┘
                 │              │              │
          dispatch/        dispatch/      dispatch/
          engineering.md   quality-       intelligence.md
                           security.md
                 └──────────────┼──────────────┘
                                │
                    ┌───────────▼───────────┐
                    │  dispatch/GENERAL.md  │ ← cross-dept handoffs
                    │  dispatch/HALT.md     │ ← emergency stop
                    │  memory/             │ ← institutional knowledge
                    └──────────────────────┘
```

---

## What is PA·co?

PA·co (Penguin Alley Commander/Officer) is a framework for building multi-agent AI systems using only markdown files. Define agents, set up coordination, and let Claude Code run your operations autonomously.

**No code. No databases. No message queues. Just markdown.**

```
You get:
- 3-16 specialized AI agents with clear roles
- A dispatch system for agent-to-agent coordination
- Institutional memory that grows smarter over time
- Quality gates that catch mistakes before you see them
- An emergency halt system so you stay in control
- Scheduled tasks for 24/7 autonomous operations
```

## Why PA·co?

| Problem | PA·co Solution |
|---------|---------------|
| AI agents step on each other's work | **Dispatch system** — file-based coordination with department isolation |
| Agents repeat the same mistakes | **Institutional memory** — every mistake becomes a permanent rule |
| Can't stop agents when things go wrong | **HALT system** — pause any department instantly |
| No quality control on agent output | **Auditor agent** — quality gates before anything reaches you |
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

## How It Works

### Agents
Each agent is a markdown file in `.claude/agents/` that defines a role:

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

### Dispatch System
Agents coordinate through simple markdown files:

```
dispatch/
  HALT.md          ← Emergency stop (CEO only)
  GENERAL.md       ← Cross-department coordination
  engineering.md   ← Engineering internal
  growth.md        ← Growth internal
```

Every agent reads `GENERAL.md` + their department file at session start, updates both at session end. No database. No API. Just files.

### Memory
Knowledge persists across sessions in `memory/`:

```
memory/
  MEMORY.md              ← Index of everything
  lessons-learned.md     ← Mistakes → permanent rules
  decisions/             ← Decision logs with reasoning
```

### Emergency Halt
```markdown
# dispatch/HALT.md

| Department | Status | Reason |
|---|---|---|
| engineering | HALTED | CEO reviewing legal blockers |
| growth | ACTIVE | — |
```

Any agent in a HALTED department stops immediately. Only the CEO can halt/resume.

## Templates

| Template | Agents | Best for |
|----------|--------|----------|
| `solo-founder` | 4 (orchestrator, builder, devops, marketer) | Solo builders shipping fast |
| `startup` | 8 (adds QA, security, researcher, strategist) | Small teams with product-market fit goals |
| `full-team` | 16 (all departments) | Mature operations with governance |
| `agency` | Customizable per client | Agencies managing multiple projects |

## Comparison

| Feature | PA·co | CrewAI | LangGraph | AutoGen |
|---------|-------|--------|-----------|---------|
| Language needed | None (markdown) | Python | Python | Python |
| Setup time | 5 minutes | Hours | Hours | Hours |
| State management | File-based dispatch | In-memory/DB | State machine | Messages |
| Department structure | Built-in | DIY | DIY | DIY |
| Quality gates | Built-in | None | None | None |
| Emergency halt | Built-in | None | None | None |
| Institutional memory | Built-in | RAG (optional) | None | None |
| Cost | $0 extra | API costs | API costs | API costs |

## Battle-Tested

PA·co isn't theoretical. We built and operate [Penguin Alley](https://penguinalley.com) entirely with PA·co:

- **16 agents** across 5 departments
- **8 products** launched (1 Tier 1 SaaS + 7 micro-tools) in 72 hours
- **66+ build sessions** with zero human coding
- **24/7 autonomous operations** via Claude Desktop scheduled tasks
- **350+ distribution targets** across directories, roundups, and communities
- **$0 infrastructure cost** — all free tiers

Every pattern in this framework comes from real production experience. [Read the full case study →](examples/saas-product/README.md)

## Documentation

- [Getting Started](docs/getting-started.md) — Full setup guide
- [Concepts](docs/concepts.md) — How dispatch, departments, and memory work
- [Adding Agents](docs/adding-agents.md) — Create custom agents for your needs
- [Department Setup](docs/department-setup.md) — Configure departments and cross-dept communication
- [FAQ](docs/faq.md) — Common questions

## Requirements

- **Claude Code** (CLI, Desktop app, or VS Code extension)
- **Claude Desktop MAX** ($100/mo) for scheduled tasks (optional — can run agents manually without it)
- Any project type: SaaS, agency, content, dev tools, research, etc.

## License

MIT — use it however you want.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome:
- New agent templates
- New department configurations
- Industry-specific templates (content agency, e-commerce, dev team, etc.)
- Documentation improvements
- Bug reports and feature requests

---

**Built by [Penguin Alley](https://penguinalley.com)** — "An easier way to live."
