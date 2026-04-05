# PA·co Concepts

Understanding how the system works before you customize it.

---

## The mental model

PA·co is a coordination layer, not a code framework. It gives each AI agent:
- A defined role (what it owns, what it doesn't touch)
- A shared mailbox (dispatch files to read and write)
- A persistent memory (files that survive between sessions)
- An emergency stop (HALT system)
- A quality gate (the auditor agent)

Every agent is just Claude Code with instructions. The "team" emerges from how those instructions coordinate through shared files.

---

## Agents

An agent is a markdown file in `.claude/agents/`. When you tell Claude Code "run as /builder," it reads that file and operates by its rules for the entire session.

### What an agent file contains

```yaml
---
name: "Builder"
model: "sonnet"
tools: ["Bash", "Read", "Write", "Glob", "Grep"]
maxTurns: 40
department: "engineering"
expected_frequency: "hourly"
---

You are the Builder for [Project].

## MISSION
Write code and ship products. That's it.

## JURISDICTION
I DO: write code, run migrations, deploy, debug
I DO NOT: write marketing copy, evaluate ideas, monitor production

## PROCESS
1. Read dispatch/HALT.md — am I halted?
2. Read dispatch/GENERAL.md — any decisions that affect me?
3. Read dispatch/engineering.md — what's my queue?
4. Do the work
5. Update dispatch/engineering.md with activity log
6. If another department needs to know: update GENERAL.md

## RULES
- Never commit secrets to git
- Test before deploying
- Always update dispatch at session end
```

### Key design principle: jurisdiction

Every agent has a clear list of what it does and what it explicitly does NOT do. This prevents two agents from both "marketing" or both "monitoring." Jurisdiction is what makes the system work — without it, agents step on each other.

### Agent types by frequency

| Type | Frequency | Example |
|------|-----------|---------|
| Core operational | Hourly | Builder (build sessions) |
| Regular cadence | Daily | DevOps (monitoring), Marketer (content) |
| On-demand | When needed | Researcher, Analyst |
| Weekly | Once per week | Finance review, weekly report |

---

## The Dispatch System

Dispatch is how agents communicate without talking to each other directly. It's a set of markdown files agents read at session start and update at session end.

### File structure

```
dispatch/
  HALT.md           ← Emergency stop. ALL agents read this FIRST.
  GENERAL.md        ← Cross-department. ALL agents read this.
  engineering.md    ← Engineering internal only.
  growth.md         ← Growth internal only.
  [dept].md         ← One file per department.
```

### HALT.md — the emergency stop

Every agent reads `HALT.md` before anything else. If its department status is `HALTED`, it stops immediately and logs the halt.

```markdown
| Department | Status  | Reason                      |
|------------|---------|-----------------------------|
| engineering | HALTED | CEO reviewing security issue |
| growth      | ACTIVE  | —                           |
```

Only you (the CEO) can halt or resume departments. Agents cannot halt each other.

### GENERAL.md — the shared whiteboard

Cross-department coordination lives here. When the Builder finishes a product and wants the Marketer to create a launch post, it writes to GENERAL.md:

```markdown
## Cross-Department Handoffs
| Date       | From      | To       | Action                          | Status  |
|------------|-----------|----------|---------------------------------|---------|
| 2026-03-28 | Builder   | Marketer | InvoiceGen LIVE at /invoicegen  | PENDING |
```

The Marketer reads this at their next session start and picks it up.

**Rule:** Only put cross-department items in GENERAL.md. Internal notes stay in department dispatches.

### Department dispatches — internal coordination

Each department has its own dispatch file. It tracks:
- Agent health (last heartbeat, expected frequency, status)
- Pending tasks with priority
- Activity log (clears daily — this is current state, not history)

```markdown
## Pending Tasks
| Priority | Agent   | Task                              |
|----------|---------|-----------------------------------|
| HIGH     | Builder | Add cookie consent banner to app  |
| MEDIUM   | DevOps  | Verify SSL renewal on prod domain |

## Activity Log (clears daily)
| Time  | Agent   | Action              | Result |
|-------|---------|---------------------|--------|
| 14:30 | Builder | Added consent banner | Done, deployed |
```

### Size limits are not optional

Dispatch files have hard line limits (GENERAL: 120 lines, department: 80 lines). These limits exist because agents read these files at every session — if they grow unbounded, agents spend half their context window on stale history. When a task is done, remove its detail row. Keep only a one-line summary. Archive details elsewhere if needed.

---

## Memory

Memory is the system's knowledge base. It lives in `memory/` and persists forever (sessions are ephemeral — files are not).

### Core files

**`memory/MEMORY.md`** — the index. One line per file, describing what it contains. Agents use this to find what they need without reading every file.

```markdown
## Active Reference
- lessons-learned.md — mandatory read for builders. Every past mistake.
- decisions/2026-03-pricing.md — pricing strategy approved by CEO.
- market-intel/competitor-scan.md — competitive landscape, updated weekly.
```

**`memory/lessons-learned.md`** — the most important file in the system. Every mistake an agent makes gets logged here with:
- What happened
- Why it happened
- The permanent rule that prevents it from happening again

Agents are required to read this before every build or deploy. This is how the system gets smarter over time.

**`memory/decisions/`** — decision logs. When an agent makes a significant decision (tech stack choice, pricing model, kill a project), it logs it here with reasoning. This prevents agents from relitigating settled decisions and gives you an audit trail.

### Memory rules

- Sessions end. Memory files don't. If it's not in memory, it didn't happen.
- Memory files are never deleted — only archived with an `_archived_` prefix.
- The MEMORY.md index must stay under 80 lines. When it grows, consolidate or archive stale entries.

---

## The HALT System

The HALT system is how you stop agents when something goes wrong.

### When to use it

- Security issue discovered that needs your review before agents continue
- Legal concern that requires your input
- Agent went off the rails and you need to course-correct
- You want to pause work while you change strategy

### How to halt

Tell Claude Code:
```
Run as /paco — halt the engineering department. Reason: reviewing security finding.
```

PA·co updates `dispatch/HALT.md`. Next time any engineering agent starts a session, they see `HALTED`, stop work, and log the halt.

### How to resume

```
Run as /paco — resume the engineering department.
```

### What agents do when halted

They stop before doing any work. They log in their department dispatch: "Session halted — [reason]. Waiting for CEO resume." They do nothing else.

---

## Quality Gates

The auditor agent is the system's quality control. It reviews significant outputs before they reach you.

### When the auditor runs

- Before a product deploys to production
- After a major feature is complete
- When an agent flags something for review (cross-department GENERAL.md handoff)
- On a weekly audit schedule (optional)

### What the auditor checks

The auditor reads `docs/quality-gates.md`, which defines checklists per output type:

- **Code deploys:** no raw errors shown to users, no secrets in code, mobile responsive, analytics configured
- **Research outputs:** claims backed by data, sources linked, competitive landscape covered
- **Marketing content:** brand voice consistent, no false claims, platform specs match
- **Specs and plans:** measurable milestones, cost model included, risks documented

### Auditor findings

The auditor writes findings to `dispatch/quality-security.md`. Engineering reads this at session start. A BLOCKER finding means the deploy is paused until resolved.

---

## The Orchestrator (PA·co)

The orchestrator (`paco.md`) is the master coordinator. It doesn't do the work — it ensures the work gets done.

**What it does:**
- Runs the daily standup (reads all dispatch files, checks all agent health)
- Routes cross-department handoffs (ensures nothing falls through the cracks)
- Identifies blockers and escalates to you
- Sends email reports (daily summary, weekly review)
- Manages the HALT system when you ask

**What it doesn't do:**
- Write code (that's Builder)
- Create content (that's Marketer)
- Monitor infrastructure (that's DevOps)

The orchestrator is the team lead, not the doer.

---

## How it all fits together

A typical day in the system:

```
9:00 AM  — Orchestrator (standup) reads all dispatches. Identifies 2 pending tasks.
            Writes handoffs in GENERAL.md for Builder and Marketer.

10:00 AM — Builder session starts.
            Reads HALT.md (ACTIVE), GENERAL.md (sees task), engineering.md (queue).
            Builds the feature. Updates engineering.md. Adds handoff to GENERAL.md
            for Auditor: "Feature X ready for review."

10:30 AM — Auditor reads GENERAL.md. Sees review request. Runs quality checks.
            No blockers found. Updates quality-security.md: "APPROVED — deploy."
            Adds to GENERAL.md: "Feature X approved for deploy."

11:00 AM — Builder (next session). Reads GENERAL.md. Sees approval. Deploys.
            Updates engineering.md with deploy confirmation.
            Adds to GENERAL.md for DevOps: "New deploy on prod, verify."

12:00 PM — DevOps reads GENERAL.md. Sees deploy. Verifies health endpoint, SSL.
            Updates engineering.md: "Deploy verified, all healthy."
```

No agent has to know what the others are doing in real time. The dispatch files are the shared context that makes coordination possible.

---

Next: [Architecture](architecture.md) — technical system design | [A2A Protocol](a2a-protocol.md) — how agents coordinate work | [Subagents API](subagents.md) — spawn agents via the Claude Agent SDK | [MCP Transports](mcp-transports.md) — connect to external tools | [Adding Agents](adding-agents.md) — create custom agents for your needs.
