# FAQ

Common questions about PA·co Framework, multi-agent systems, and Claude Code operations.

---

## Setup and Requirements

### What is PA·co Framework?

PA·co Framework is a markdown-first, zero-code multi-agent operations system for Claude Code. It enables 3-16 specialized AI agents to coordinate via file-based state management, maintain institutional memory through 4-layer Context Engineering, and operate autonomously with human oversight. PA·co stands for Penguin Alley Commander/Officer.

### What model do I need?

Any model that runs in Claude Code works. The practical recommendation:

| Use case | Model | Why |
|----------|-------|-----|
| Critical agents (auditor, security) | Opus | These make quality gate decisions -- worth the cost |
| General agents (builder, marketer, researcher) | Sonnet | High quality, much lower cost than Opus |
| Lightweight agents (devops health checks, standup) | Sonnet or Haiku | Short read-and-report tasks |

If you are cost-conscious, all-Sonnet works well. The system is designed so agent quality comes from good instructions, not just model capability.

### How much does it cost to run PA·co?

PA·co itself costs nothing. You pay for:

- **Claude usage** -- each agent session consumes tokens from your Claude account. Cost depends on how many agents run and how often.
- **Claude Pro or MAX** -- MAX ($100-200/mo) required for scheduled autonomous tasks. Pro ($20/mo) works for manual triggering.
- **External services** -- databases, hosting, email providers that your agents use. These are project costs, not PA·co costs.

A solo founder running 4 agents on daily schedules typically uses 500K-2M tokens per day. With MAX, this is covered by the flat subscription.

### Can I use GPT-4 or Gemini instead of Claude?

No. PA·co is built specifically for Claude Code. The agent file format (YAML frontmatter + markdown instructions), the tool access (Bash, Read, Write, Grep, Glob), and the scheduled task system are all Claude Code features. For multi-LLM support, consider CrewAI or LangGraph.

### Do I need Claude Desktop MAX for scheduled tasks?

Yes, for fully autonomous operation (agents running on a schedule without you triggering them). Without MAX, you can still use PA·co by triggering agents manually:

```
Run as /researcher -- scan for market opportunities in developer tools.
```

This is perfectly fine for early-stage or low-frequency workflows. Many users start manual and upgrade to MAX when the volume justifies it.

### What operating systems does PA·co support?

PA·co works anywhere Claude Code runs: macOS, Windows, and Linux. The framework itself is just markdown files, so there are no OS-specific dependencies.

### Can I use PA·co with VS Code or JetBrains?

Yes. Claude Code is available as a CLI, desktop app, VS Code extension, and JetBrains extension. PA·co works with all of these. Scheduled tasks require the CLI or desktop app.

### How do I update PA·co to a new version?

Pull the latest version from GitHub and merge it into your project. PA·co uses markdown files, so updates are just file changes. Your customizations (agent definitions, state files, product configs) are separate from the framework core and will not be overwritten.

---

## Agents and Architecture

### How many agents should I start with?

Start with three to four. More agents means more coordination overhead. You want to feel the value before adding complexity.

Recommended starting set for a solo founder:
1. **Orchestrator** (PA·co) -- always required
2. **Builder** -- if you are building a product
3. **DevOps** -- if you are deploying to production
4. **Marketer** -- if you are acquiring users

Add more when those four cannot keep up.

### What is the maximum number of agents?

PA·co recommends 3-16 agents. The upper limit is not technical but practical: more than 16 agents creates coordination overhead that outweighs the benefits. In production, Penguin Alley runs 12 agents across 5 departments, which is the sweet spot for a multi-product operation.

### What are departments and why do they matter?

Departments group related agents and define coordination boundaries. A typical setup includes:

- **Executive** -- orchestrator (PA·co)
- **Engineering** -- builder, designer
- **Quality and Security** -- QA, security auditor, auditor
- **Intelligence and Strategy** -- researcher, strategist
- **Growth and Revenue** -- marketer, sales

Departments matter because they define who talks to whom. Agents within a department share dispatch files. Cross-department coordination goes through the orchestrator or general dispatch.

### What if two agents conflict on a decision?

The state management system is designed to prevent this. The rule: agents check shared state files before making decisions that affect other departments. When conflicts do happen:

1. The orchestrator identifies the conflict during standup
2. It writes a conflict note to the general dispatch
3. The CEO (you) makes the final call
4. The orchestrator updates state with the resolution

The CEO is always the tiebreaker.

### How do I restrict which tools an agent can use?

Use the `tools_allowed` and `tools_denied` fields in the agent's YAML frontmatter. `tools_allowed` is a strict whitelist (only those tools are available). `tools_denied` blocks specific tools while keeping the rest. Common pattern: auditors get `tools_allowed: ["Read", "Glob", "Grep"]` (read-only), researchers get `tools_denied: ["Write", "Edit"]` (no file modification). This maps to the Anthropic Subagents API's per-agent tool restrictions. See `core/agent-schema.md` for resolution logic and patterns.

### Can agents create other agents?

Yes. In PA·co production, agents have created new sub-agents, modified existing agents, and updated CLAUDE.md -- all autonomously. However, structural changes like adding agents should be reviewed by the orchestrator during standup so the system stays coherent.

### What happens if an agent makes a mistake?

The system has three defenses:

1. **Quality gates** -- the auditor reviews outputs before they reach production. A mistake caught here never ships.
2. **Lessons learned** -- when a mistake gets through, it is logged as a permanent rule. Same mistake cannot happen twice if the rule is written clearly.
3. **HALT system** -- if an agent goes seriously off the rails, you halt its department immediately and review before resuming.

### How do agents share information?

Via state files and dispatch files:

- **Immediate sharing** (needs action this session): write to dispatch files with a handoff for the relevant agent.
- **Persistent knowledge** (useful for future sessions): store in the vector database (pgvector) or memory files.
- **Decisions with reasoning**: store in the vector database tagged as decisions, preventing agents from relitigating settled questions.

### What is the difference between dispatch and state?

**State** (STATE.md) tracks what IS: current phase, progress, bugs, last_actor. It is the source of truth for where a product stands.

**Dispatch** (DISPATCH.md) tracks what HAPPENED and what NEEDS TO HAPPEN: session results, handoffs between agents, and pending tasks for other departments.

State is read by every agent. Dispatch is read mainly by the agent it is addressed to.

---

## Context Engineering

### What is Context Engineering?

Context Engineering is PA·co's system for ensuring each AI agent gets the right information at the right time without exceeding context window limits. It uses four layers:

1. **Identity** -- who the agent is (role definition, organizational rules)
2. **State** -- what is happening now (product progress, pipeline status)
3. **Relevant** -- what the agent needs to know for this specific session (semantic search results)
4. **Archive** -- everything else, available if search queries change

### Why not just put everything in the prompt?

Context windows have limits (even with 1M tokens). More importantly, irrelevant context degrades agent performance. An agent that receives 200K tokens of context performs worse than one that receives 10K tokens of precisely relevant context. Context Engineering filters information so agents focus on what matters.

### Do I need a vector database?

No. PA·co works without a vector database using markdown files for all knowledge storage. The vector database (pgvector via Supabase) is optional and adds the Relevant and Archive layers for semantic search. Start without it. Add it when your knowledge base outgrows what fits in markdown files.

### How does pgvector integration work?

PA·co uses Supabase's pgvector extension for semantic search. Knowledge is embedded and stored with metadata (type, scope, source). When an agent needs context, a search query returns the 5-10 most relevant results. This is Layer 3 (Relevant) of Context Engineering.

Setup requires a Supabase project with pgvector enabled. See [core/context-engineering.md](../core/context-engineering.md) for the full specification.

### What is the difference between memory files and vector database?

**Memory files** (markdown) are simple, human-readable, and require no infrastructure. Good for small projects with limited knowledge.

**Vector database** (pgvector) enables semantic search across large knowledge bases. Good for projects with hundreds of lessons, decisions, and competitive intel entries. Knowledge that would be too much for markdown files gets embedded and searched contextually.

### How does same agent + different context work?

Agent definitions are generic: a Builder knows how to write code, run migrations, and deploy. But each product has its own `products/{name}/CLAUDE.md` that defines the tech stack, coding rules, and deployment targets. The same Builder agent behaves differently for a Next.js SaaS versus a Python CLI tool because it receives different product context.

---

## Workflow and Phases

### What is the 7-phase workflow?

Every product goes through seven phases:

1. **Research** -- find problems worth solving (not solutions)
2. **Refine** -- all departments enrich the specification in parallel
3. **Post-Refine** -- auditor reviews everything; fix or kill
4. **CEO Gate** -- human approves, rejects, or defers
5. **Develop** -- build from specs with Build/QA alternation
6. **Deploy** -- ship, scan, verify
7. **Evolve** -- continuous improvement, competitive defense, iteration

### Can I skip phases?

No. The full workflow applies to every product. This is a core design principle. Skipping phases is how bad products ship. The Research phase prevents building solutions to nonexistent problems. The CEO Gate prevents unauthorized work. Quality gates prevent defective code from deploying.

### What is the CEO Gate?

The CEO Gate is Phase 4, where the human operator reviews everything produced in Phases 1-3 and decides: approve (GO), reject (KILL), or defer (HOLD). No product advances to development without explicit human approval. This is the primary human-in-the-loop mechanism.

### What happens if the CEO does not respond to the gate?

PA·co has a configurable timeout (default 48 hours). After timeout, the product can be auto-approved with enhanced oversight: QA runs every session (not alternating), and the auditor reviews every 3rd build session. Deploy still requires human verification -- auto-approve never extends to deployment.

### What is Build/QA alternation?

During the Develop phase, build and QA sessions alternate automatically. After the Builder completes work, it sets `last_actor: "builder"` in STATE.md. The next session sees this and runs QA instead of building. After QA passes, it sets `last_actor: "qa"`, and the Builder runs next.

This guarantees every piece of code is reviewed before more code is written.

### How do products move between phases?

Phase transitions happen when the gatekeeper for that phase approves the transition. The orchestrator updates PIPELINE.md with the new phase, and the relevant agents pick up work in their next scheduled session.

### Can multiple products be in development at the same time?

PA·co enforces one product in active development (Phases 1-6) at a time to maintain focus. Multiple products can be in Evolve (Phase 7) simultaneously. This prevents context switching and ensures each product gets full attention through the pipeline.

---

## Running the System

### How do I know if an agent is stuck?

Each agent updates dispatch files with activity logs at session end. During standup, the orchestrator checks last heartbeat vs expected frequency. If an agent that runs daily has not logged activity in 48 hours, the orchestrator flags it.

### How do I give agents new instructions?

Three options depending on scope:

- **Permanent rule** (all future sessions): add it to the agent's markdown file in `agents/`. Changes take effect immediately on next session.
- **Project-wide rule** (all agents): add it to `CLAUDE.md` or create an executive order.
- **One-time task** (this session only): add it to the relevant dispatch file under Pending Tasks.

### Can I run multiple agents simultaneously?

Multiple Claude Code sessions can run in parallel. To avoid file conflicts, agents should write to different files. The scheduled task system serializes agents -- each task runs in its own session at different times.

### How do I reset an agent that went wrong?

1. Clear the agent's activity log in its dispatch file
2. Remove any incomplete handoffs it left
3. Correct any bad data in state files or vector database
4. Re-trigger the agent: "Run as /[agent] -- start fresh. Previous session had issues."

For severe cases, run the orchestrator in audit mode to identify all inconsistencies.

### How do I stop everything immediately?

Edit `state/HALT.md`:
```markdown
## Current: HALT ALL
Reason: [your reason]
```

Every schedule reads HALT.md before doing anything. All agent operations stop within one schedule cycle (typically under an hour for hourly schedules, immediately for manually triggered agents).

### What is the standup and why does it matter?

The standup is a daily scheduled session where the orchestrator reviews all agent activity, identifies conflicts, surfaces blockers, and prepares context for the CEO. It is the heartbeat of the system -- if the standup runs, the system is healthy.

---

## Production Use

### Is PA·co used in production?

Yes. PA·co runs Penguin Alley's entire operations: 12 agents across 5 departments, 19 scheduled tasks running 24/7, multiple products shipped through the full pipeline. Every pattern in this framework comes from real production experience.

### What are the biggest failure modes?

From production experience:

1. **File growth** -- agents append without archiving. Files hit size limits and agents cannot read them properly. Fix: enforce size limits aggressively with automated cleanup.
2. **Knowledge rot** -- stale information that contradicts current state. Agents act on outdated context. Fix: date-stamp knowledge entries and review regularly.
3. **Jurisdiction drift** -- agents start doing work outside their defined role. Fix: quarterly jurisdiction review.
4. **No measurement** -- agents define goals but nobody checks if they are achieved. Fix: every goal gets a metric, a source, and a review frequency.

### How do I know PA·co is actually helping?

Check the weekly report output. It should answer: what shipped this week? What metrics moved? What was learned? What is blocked? If the report is full of activity but no outcomes, agents are busy but not productive.

### What kinds of projects work best with PA·co?

PA·co works for any project type: SaaS products, developer tools, content operations, agency work, research projects, and e-commerce. It works best when:
- You have recurring work that benefits from automation
- Your project has distinct phases (research, build, test, deploy)
- You want to maintain quality while moving fast
- You are comfortable with Claude Code as your development environment

### Can PA·co build mobile apps?

PA·co can coordinate agents that build mobile apps (React Native, Flutter, etc.), but Claude Code itself works best with web technologies. Mobile development through PA·co typically uses cross-platform frameworks deployed via web-based CI/CD.

### How does PA·co handle secrets and API keys?

Secrets are stored in `.env` files (never committed to git). Agents access secrets through environment variables. PA·co has explicit rules: agents have zero spending authority, and any action requiring API keys or payments goes through the CEO Gate as a blocker.

---

## Comparison with Other Approaches

### How is PA·co different from just using Claude Code directly?

Using Claude Code directly gives you one conversation with one AI. PA·co gives you a structured team of specialized agents, each with persistent memory, defined roles, and coordinated workflows. The difference is like having one generalist employee vs a department of specialists with a project management system.

### How is PA·co different from CrewAI?

CrewAI is a Python SDK for building multi-agent systems with any LLM. PA·co is a markdown-only framework for Claude Code. CrewAI requires writing Python code; PA·co requires writing markdown files. CrewAI supports multiple LLMs; PA·co is Claude-only. CrewAI focuses on task execution; PA·co focuses on product lifecycle management.

See [comparisons.md](comparisons.md) for a detailed comparison.

### How is PA·co different from LangGraph?

LangGraph models agent workflows as directed graphs in Python with fine-grained control over execution flow. PA·co uses a fixed 7-phase workflow with quality gates. LangGraph is more flexible but requires more setup. PA·co is more opinionated but works out of the box.

### Does PA·co support the A2A (Agent-to-Agent) protocol?

PA·co solves the same coordination problem as Google's A2A protocol using file-based patterns instead of runtime message passing. Agents coordinate through shared state files (turn-based alternation, cross-department handoffs, escalation chains, pipeline phase gates, and priority overrides). If you need to integrate with external A2A-compatible agents, build a bridge agent that translates between runtime messages and PA·co's file-based state. Full details: [A2A Protocol](a2a-protocol.md).

### Can I use PA·co alongside other frameworks?

Not recommended. PA·co and other multi-agent frameworks solve the same coordination problem. Running both creates conflicting state management and coordination overhead. Pick one approach.

### Is PA·co suitable for enterprise use?

PA·co is designed for solo founders and small teams (1-10 people). It has strong governance features (CEO Gate, quality gates, emergency halt) but does not have enterprise features like SSO, external audit logging, or SLA guarantees. For enterprise needs, consider CrewAI Enterprise.

---

## Troubleshooting

### Agent says it cannot do something because it is not in its jurisdiction

That is correct behavior. Either route the task to the right agent, update the agent's I DO section to include the task, or explicitly override for one session.

### Agent created files in the wrong location

Add a file structure rule to the agent's markdown file under a File Locations section. Be explicit about where reports, decisions, and code go.

### Agent keeps re-reading files without doing anything

The agent's process section is too vague. Make it explicit: read this file, find tasks with status PENDING, pick the highest priority one, execute it, mark it DONE.

### I want to pause the whole system for a week

Set HALT ALL in `state/HALT.md`. When you return, change it to CLEAR and run a standup to catch up on what is pending.

### How do I debug a specific agent session?

1. Read the agent's dispatch file for its last activity log
2. Check STATE.md for the product it was working on
3. Check CEO_BLOCKERS.md for anything it flagged
4. Re-run the agent manually with verbose instructions: "Run as /[agent] -- explain your reasoning at each step"

### My vector database queries return irrelevant results

Check the metadata on your stored entries. Each entry should have type (lesson, decision, competitive_intel), scope (universal, product_specific), and source. Queries work best when they match the natural language of the stored content. Re-embed entries with better metadata if needed.

---

## Claude Agent SDK & Subagents

### Can I spawn PA·co agents programmatically?

Yes. The Claude Agent SDK lets you define PA·co agents as `AgentDefinition` objects and spawn them via `query()`. Each agent gets isolated context, restricted tools, and can run in parallel. Your PA·co agent schema fields (`tools_allowed`, `tools_denied`, `model`, etc.) map directly to SDK fields. See [docs/subagents.md](subagents.md) for the full mapping and examples.

### Do I need the SDK to use PA·co?

No. PA·co's default mode is file-based: agents are `.claude/agents/*.md` files triggered by Claude Code sessions or scheduled tasks. The SDK is an optional integration for custom applications, CI/CD pipelines, or when you need programmatic control over agent spawning.

### Can SDK subagents use PA·co's dispatch coordination?

Yes. Subagents read and write files like any Claude Code session. They coordinate through the same STATE.md, PIPELINE.md, and dispatch files. The SDK adds a programmatic spawn mechanism; the coordination patterns (turn-based alternation, cross-department handoffs, escalation chains) remain file-based.

### Do SDK subagents enforce tool restrictions?

Yes, at the API level. When you pass `tools=["Read", "Glob", "Grep"]` to an `AgentDefinition`, the subagent physically cannot call Edit, Write, or Bash. This is stronger than file-based tool declarations, which rely on the agent following its instructions.

---

Back to: [Getting Started](getting-started.md) | [Concepts](concepts.md) | [A2A Protocol](a2a-protocol.md) | [Subagents API](subagents.md) | [Adding Agents](adding-agents.md) | [Comparisons](comparisons.md)
