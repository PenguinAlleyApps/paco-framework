# PA·co Framework

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Claude Code](https://img.shields.io/badge/Claude_Code-Required-blue.svg)
![Status](https://img.shields.io/badge/Status-v2.0-brightgreen.svg)
![Agents](https://img.shields.io/badge/Agents-3_to_16+-purple.svg)

## What is PA·co Framework?

**PA·co Framework is a markdown-first, zero-code multi-agent operations system for Claude Code.** It enables 3-16 specialized AI agents to coordinate via file-based state management, maintain institutional memory through 4-layer Context Engineering, and operate autonomously with human oversight -- without writing a single line of Python.

PA·co stands for **P**enguin **A**lley **Co**mmander/Officer. It transforms a Claude Code instance into an autonomous team of AI agents that coordinate, learn, and evolve using only markdown files.

### How PA·co Framework Works

PA·co uses a file-based architecture where each AI agent reads markdown files to understand its role, the current system state, and what work needs to be done. Agents coordinate through shared state files rather than message passing:

```
                         +---------------+
                         |     CEO       |
                         |   (Human)     |
                         +-------+-------+
                                 | halt / resume / approve
                         +-------v-------+
                         |    PA-co      |
                         | Orchestrator  | <- 4-layer context
                         +-------+-------+
                 +---------------+---------------+
                 |               |               |
          +------v------+ +-----v-----+ +-------v------+
          | Engineering | |   Q & S   | | Intelligence | ...
          |             | |           | |              |
          | Builder     | | QA        | | Researcher   |
          | Designer    | | Auditor   | | Strategist   |
          +------+------+ +-----+-----+ +-------+------+
                 |               |               |
          products/         state/          catalogs/
          {name}/STATE      PIPELINE.md     sectors.md
                            HALT.md         tech-stacks.md
```

### Key Capabilities

| Capability | Description |
|-----------|-------------|
| **Multi-agent coordination** | 3-16 specialized AI agents organized into departments, each with clear roles, jurisdictions, and handoff protocols |
| **7-phase product workflow** | Structured pipeline from Research to Refine to Post-Refine to CEO Gate to Develop to Deploy to Evolve |
| **4-layer Context Engineering** | Identity, State, Relevant, Archive -- ensures every agent session receives precisely the context it needs |
| **Quality gates** | Mandatory checks at every phase transition, preventing defects from propagating |
| **Emergency halt system** | Instantly pause any product or all operations with a single markdown edit |
| **Human-in-the-loop governance** | CEO approval gates for critical decisions; agents operate autonomously within defined boundaries |
| **Zero-code setup** | Everything is configured through markdown files -- no Python, no YAML configs, no infrastructure code |

---

## Quick Start

1. Clone this repo into your project
2. Run the bootstrap prompt in Claude Code:
   ```
   Read paco-bootstrap.md and execute the setup
   ```
3. Answer 5-7 questions about your project
4. PA·co generates your entire multi-agent system
5. Run your first standup: `Run as /paco -- execute daily standup`

Full setup guide: [docs/getting-started.md](docs/getting-started.md)

---

## Architecture

### 7-Phase Product Workflow

Every product goes through the full workflow. No shortcuts, no skipped phases.

```
RESEARCH -> REFINE -> POST-REFINE -> CEO GATE -> DEVELOP -> DEPLOY -> EVOLVE
```

| Phase | What happens | Gatekeeper |
|-------|-------------|------------|
| **Research** | Find problems worth solving. Scan market sectors. Output: specification template. | PA·co |
| **Refine** | All departments enrich the spec in parallel. Engineering defines the solution. Each agent asks minimum 10 questions with mandatory web search. | PA·co |
| **Post-Refine** | Auditor reviews all specs. Fix issues or kill the product. | Auditor |
| **CEO Gate** | Human approves, rejects, or defers. No product advances without human approval. | CEO |
| **Develop** | Builder + Designer build from specs. No improvisation. Build/QA alternation enforced. | QA + Security |
| **Deploy** | Ship to production. Security scan. Health verification. | CEO |
| **Evolve** | Continuous improvement: health reviews, competitive defense, feature iteration. | Auditor (biweekly) |

See [core/workflow-schema.md](core/workflow-schema.md) for the full schema.

### 4-Layer Context Engineering

Context Engineering is the core innovation of PA·co Framework. It solves the fundamental problem of multi-agent AI systems: how does each agent get the right information at the right time without exceeding context limits?

| Layer | What it provides | Source | Lifecycle |
|-------|-----------------|--------|-----------|
| **Identity** | CLAUDE.md + agent definition + role catalogs | Repository files | Read-only per session |
| **State** | Product STATE.md + Pipeline + today's dispatch | `state/`, `products/*/` | Rewritten every session |
| **Relevant** | Semantic search results from vector database | pgvector (Supabase) | ~5-10 results per query |
| **Archive** | All historical knowledge not returned by search | Vector database | Grows indefinitely |

**Same agent + different context = different behavior per product.** Agent definitions are generic; `products/{name}/` directories make them product-specific.

See [core/context-engineering.md](core/context-engineering.md) for the full specification.

### State Management

Products track their own state. A global pipeline tracks all products.

```
state/
  PIPELINE.md        -- All products and their current phase
  HALT.md            -- Emergency stop system
  CEO_BLOCKERS.md    -- Items requiring human decision

products/{name}/
  CLAUDE.md          -- Product-specific rules and stack
  STATE.md           -- Progress, bugs, last_actor, metrics
  DISPATCH.md        -- Cross-department handoffs
  mvp-specs/         -- What to build (specifications)
```

Build/QA alternation is enforced via the `last_actor` field in STATE.md: if the last actor was the Builder, QA runs next, and vice versa. This guarantees every build session is followed by a quality check.

See [core/state-schema.md](core/state-schema.md) for the full schema.

### Agent Architecture

Each agent is defined as a markdown file with YAML frontmatter:

```yaml
---
name: "Builder"
department: "engineering"
expected_frequency: "hourly"
---

You are the Builder. Your job is to write code, deploy, and maintain products.

## I DO:
- Write code from specifications
- Run database migrations
- Deploy to production

## I DO NOT:
- Create marketing content (that is the Marketer)
- Make spending decisions (requires CEO approval)
```

PA·co supports 3-16 agents organized into departments. A typical production setup uses 8-12 agents across 5 departments: Executive, Engineering, Quality & Security, Intelligence & Strategy, and Growth & Revenue.

See [core/agent-schema.md](core/agent-schema.md) for the full schema.

### Scheduling

Agents run on schedules via Claude Code scheduled tasks:

| Schedule type | Examples |
|--------------|---------|
| Work hours (jornada) | Standup at 8am, Refine phases 8:30-10:30am, Competitive Defense at 2pm |
| 24/7 automation | Build sessions hourly, QA alternating, email relay |
| Weekly | Friday reports, open source sync |

Schedules include smart-skip logic: if there is nothing to do, the agent exits silently instead of generating empty output.

### Emergency Halt

The HALT system provides instant, global control over all agent operations:

```markdown
# state/HALT.md
## Current: CLEAR
```

Write `HALT [product]` or `HALT ALL` to stop operations instantly. Every schedule reads HALT.md before doing anything. Only the CEO (human operator) can halt or resume.

---

## PA·co vs CrewAI vs LangGraph vs AutoGen

PA·co Framework takes a fundamentally different approach from Python-based multi-agent frameworks. While CrewAI, LangGraph, and AutoGen require writing code to define agents and workflows, PA·co uses markdown files exclusively.

| Feature | PA·co Framework | CrewAI | LangGraph | AutoGen (retired) |
|---------|----------------|--------|-----------|-------------------|
| **Language required** | None (markdown only) | Python | Python | Python |
| **Setup time** | 5 minutes | Hours | Hours | Hours |
| **Product lifecycle management** | 7-phase workflow with gates | No built-in workflow | State machine (manual) | No built-in workflow |
| **Context management** | 4-layer Context Engineering | In-memory / optional RAG | State machine variables | Message history |
| **Quality gates** | Built-in at every phase transition | None | None | None |
| **Emergency halt** | Built-in (HALT.md) | None | None | None |
| **Knowledge persistence** | Vector DB + markdown files | Optional RAG | None built-in | None built-in |
| **Human approval gates** | CEO Gate built into workflow | None | Interrupt points (manual) | Human-in-the-loop (manual) |
| **Agent coordination** | File-based state (no race conditions) | Task delegation | Graph edges | Group chat / nested |
| **Cost model** | $0 (MIT, uses your Claude subscription) | $99-$120K/year | $39/user/mo + per-node | Free (retired) |
| **LLM support** | Claude Code only | Multi-LLM | Multi-LLM | Multi-LLM |
| **Best for** | Autonomous operations with governance | Python developers, enterprise teams | Complex agent graphs | Legacy projects |

**When to choose PA·co:** You want structured, governed multi-agent operations without writing code. You use Claude Code. You need a product lifecycle (not just task execution). You want human-in-the-loop by default.

**When to choose CrewAI:** You need multi-LLM support. Your team writes Python. You need enterprise features and support.

**When to choose LangGraph:** You need fine-grained control over agent execution graphs. You are building complex, branching agent workflows in Python.

For a detailed comparison, see [docs/comparisons.md](docs/comparisons.md).

---

## Templates

### Free Templates (included)

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

---

## Battle-Tested in Production

PA·co Framework is not theoretical. It runs [Penguin Alley's](https://penguinalley.com) entire operations:

- **12 agents** across 5 departments + Executive
- **19 scheduled tasks** running autonomously 24/7
- **4-layer Context Engineering** with pgvector semantic search
- **Multiple products** shipped through the full 7-phase pipeline
- **$0 infrastructure cost** -- built entirely on free tiers

Every pattern in this framework comes from real production experience. The 7-phase workflow, Build/QA alternation, emergency halt system, and Context Engineering layers were all developed and refined through shipping real products.

---

## Core Schemas

| Schema | What it defines |
|--------|----------------|
| [agent-schema.md](core/agent-schema.md) | Agent file structure, roles, jurisdictions |
| [context-engineering.md](core/context-engineering.md) | 4-layer context system specification |
| [workflow-schema.md](core/workflow-schema.md) | 7-phase product lifecycle |
| [state-schema.md](core/state-schema.md) | Product state and pipeline tracking |
| [dispatch-schema.md](core/dispatch-schema.md) | Cross-department handoff system |
| [memory-schema.md](core/memory-schema.md) | File-based knowledge persistence |
| [schedule-schema.md](core/schedule-schema.md) | Agent scheduling patterns |
| [executive-orders-template.md](core/executive-orders-template.md) | CEO directives template |

## Documentation

- [Getting Started](docs/getting-started.md) -- Full setup guide
- [Concepts](docs/concepts.md) -- Departments, context layers, and workflows
- [Adding Agents](docs/adding-agents.md) -- Create custom agents
- [FAQ](docs/faq.md) -- 50+ questions and answers about multi-agent systems
- [Comparisons](docs/comparisons.md) -- PA·co vs CrewAI vs LangGraph vs AutoGen

## Requirements

- **Claude Code** (CLI, Desktop app, VS Code extension, or JetBrains extension)
- **Claude Pro/Max** for scheduled tasks (optional -- can run agents manually)
- Any project type: SaaS, agency, content, dev tools, research, etc.

## License

MIT -- use it however you want.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome:
- New agent templates
- New department configurations
- Industry-specific templates
- Documentation improvements
- Bug reports and feature requests

---

**Built by [PA·co](https://penguinalley.com) -- A Penguin Alley System**
