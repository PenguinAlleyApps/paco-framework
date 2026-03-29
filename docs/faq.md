# FAQ

Common questions about PA·co.

---

## Setup & Requirements

### What model do I need?

Any model that runs in Claude Code works. The practical recommendation:

| Use case | Model | Why |
|----------|-------|-----|
| Critical agents (auditor, security) | Opus | These make quality gates decisions — worth the cost |
| General agents (builder, marketer, researcher) | Sonnet | High quality, much lower cost than Opus |
| Lightweight agents (devops health checks, standup) | Sonnet or Haiku | Short read-and-report tasks |

If you're cost-conscious, all-Sonnet works well. The system is designed so agent quality comes from good instructions, not just model capability.

### How much does it cost to run PA·co?

PA·co itself costs nothing. You pay for:

- **Claude usage** — each agent session consumes tokens from your Claude account. Cost depends on how many agents run and how often.
- **Claude Desktop MAX ($100/mo)** — required only for scheduled autonomous tasks. If you trigger agents manually, you don't need MAX.
- **External services** — databases, hosting, email providers that your agents use. These are project costs, not PA·co costs.

A solo founder running 4 agents on daily schedules typically uses 500K-2M tokens per day. At Sonnet pricing, that's roughly $3-15/day in API costs if using the API directly. With MAX, it's covered by the flat subscription.

### Can I use GPT-4 or Gemini instead of Claude?

No. PA·co is built specifically for Claude Code. The agent file format (YAML frontmatter + markdown instructions), the tool access (Bash, Read, Write, Grep, Glob), and the scheduled task system are all Claude Code features.

If you want a similar pattern for other models, you'd need to build your own runner — PA·co won't work out of the box.

### Do I need Claude Desktop MAX for scheduled tasks?

Yes, for fully autonomous operation (agents running on a schedule without you triggering them). Claude Desktop MAX is $100/mo and includes unlimited scheduled tasks.

Without MAX, you can still use PA·co by triggering agents manually:
```
Run as /researcher — scan for market opportunities in developer tools.
```

This is perfectly fine for early-stage or low-frequency workflows. Many users start manual and upgrade to MAX when the volume justifies it.

---

## Agents & Architecture

### How many agents should I start with?

Start with three to four. More agents = more coordination overhead. You want to feel the value before adding complexity.

Recommended starting set for a solo founder:
1. **Orchestrator** (PA·co) — always required
2. **Builder** — if you're building a product
3. **DevOps** — if you're deploying to production
4. **Marketer** — if you're acquiring users

Add more when those four can't keep up.

### What if two agents conflict on a decision?

The dispatch system is designed to prevent this. The rule: agents must check `dispatch/GENERAL.md` before making decisions that affect other departments. If an agent sees a relevant decision already recorded, it honors it instead of overriding it.

When conflicts do happen (they will):
1. PA·co (orchestrator) identifies the conflict during standup
2. It writes a conflict note to `dispatch/GENERAL.md`
3. You (the CEO) make the final call
4. PA·co updates both agent files and GENERAL.md with the resolution

The CEO is always the tiebreaker.

### Can agents create other agents?

Yes. In PA·co's own production system, agents have created new sub-agents, modified existing agents, and updated CLAUDE.md — all autonomously. This is part of the EO-013 (full autonomy) principle.

However, structural changes like adding agents should be reviewed by the orchestrator during standup so the system stays coherent. An agent shouldn't silently create a new agent without the orchestrator knowing.

### What happens if an agent makes a mistake?

The system has three defenses:

1. **Quality gates** — the auditor agent reviews outputs before they reach production or the CEO. A mistake caught here never ships.

2. **Lessons-learned.md** — when a mistake gets through, it's logged as a permanent rule that all agents read before relevant sessions. Same mistake cannot happen twice if the rule is written clearly.

3. **HALT system** — if an agent goes seriously off the rails, you halt its department immediately and review before resuming.

No system eliminates all mistakes. PA·co minimizes recurrence.

### How do agents share information they discover?

Via dispatch files and memory files.

- **Immediate sharing** (needs action this session): write to `dispatch/GENERAL.md` with a handoff for the relevant agent.
- **Persistent knowledge** (useful for future sessions): write to `memory/` with a description in `memory/MEMORY.md`.
- **Decisions with reasoning**: write to `memory/decisions/` — prevents relitigating settled questions.

---

## Running the System

### How do I know if an agent is "stuck" or skipped work?

Each agent updates its department dispatch with an activity log at session end. During standup, the orchestrator checks last heartbeat vs expected frequency. If an agent that runs daily hasn't logged activity in 48 hours, the orchestrator flags it.

You can also manually check:
```
Run as /paco — check agent health across all departments and report any gaps.
```

### What's the right way to give agents new instructions mid-project?

Three options depending on scope:

**Permanent rule** (applies to all future sessions): add it to the agent's file in `.claude/agents/`. Changes take effect immediately on the next session.

**Project-wide rule** (all agents): add it to `CLAUDE.md` under a relevant section, or create an executive order in `docs/executive-orders.md`.

**One-time task** (this session only): add it to the agent's department dispatch under Pending Tasks, then trigger the agent.

Avoid giving instructions by just typing them in a chat — that context is lost when the session ends.

### Can I run multiple agents simultaneously?

Technically yes — you can open multiple Claude Code sessions. In practice, simultaneous agents writing to the same dispatch file can cause conflicts. The safe approach: run agents sequentially, or ensure they write to different files.

The scheduled task system (Claude Desktop MAX) handles this by serializing agents — each task runs in its own session at different times.

### How do I reset an agent if it went wrong?

For a full reset:
1. Clear the agent's activity log in its department dispatch
2. Remove any incomplete handoffs in GENERAL.md that it left
3. If it wrote bad data to memory, manually correct or archive the affected file
4. Re-trigger the agent with a fresh context: "Run as /[agent] — start fresh. Previous session had issues. Check dispatch and resume from current state."

For a severe case where you don't know what it changed:
```
Run as /paco — audit all dispatch files and memory files for inconsistencies
or corrupted state. Report what needs to be cleaned up.
```

---

## Production Use

### Is this used in production anywhere?

Yes. PA·co runs Penguin Alley's entire operations:
- 16 agents across 5 departments
- 7 products (1 full SaaS, 6 micro-tools)
- 66+ build sessions
- 24/7 via Claude Desktop scheduled tasks

Every pattern in this framework comes from real production experience, including the failure modes.

### What are the biggest failure modes to watch for?

From production experience:

**Dispatch file growth** — Agents keep appending without archiving. Files hit their line limits and agents can't read them properly. Fix: enforce the size limits aggressively. Done tasks get removed, not annotated.

**Memory file rot** — Memory files accumulate stale information that contradicts current state. Agents act on outdated context. Fix: date-stamp memory files and review MEMORY.md monthly for stale entries.

**Jurisdiction drift** — Over time, agents start doing things outside their defined jurisdiction, often because "no one else was handling it." Fix: quarterly jurisdiction review. If an agent is doing work not in its I DO list, either update the list or reassign the work.

**No measurement** — Agents define goals but no one measures whether they're achieved. Fix: every milestone gets a metric, a source, and a review frequency. See `docs/executive-orders.md` — the EO-100 principle.

### How do I know PA·co is actually helping vs just running busy?

Check the weekly report output. It should answer:
- What shipped this week?
- What metrics moved?
- What was learned (new lessons-learned entries)?
- What's blocked?

If the report is full of activity but no outcomes, agents are busy but not productive. Tighten their process sections to focus on outputs, not activities.

---

## Troubleshooting

### "Agent says it can't do X because it's not in its jurisdiction"

That's correct behavior. The agent is following its rules. Either:
- The task belongs to a different agent → route it correctly
- The task should be in this agent's jurisdiction → update its I DO section
- The task is an exception → tell it explicitly: "Override jurisdiction for this session — do X because Y"

### "Agent created files in the wrong location"

Add a file structure rule to the agent's file:

```markdown
## File Locations
- Reports go in: `output/reports/`
- Decisions go in: `memory/decisions/`
- Never write to: `src/` or `supabase/` (builder only)
```

### "Agent keeps re-reading the same files without doing anything"

The agent's process section is too vague. "Check the dispatch" without "then do X" produces loops. Make the process explicit:

```markdown
## PROCESS
1. Read dispatch/HALT.md
2. Read dispatch/GENERAL.md
3. Read dispatch/intelligence.md — find tasks with status PENDING assigned to me
4. Pick the highest-priority pending task
5. Execute it
6. Mark it DONE in dispatch
7. Add result to activity log
```

### "I want to pause the whole system for a week"

Halt all departments:
```
Run as /paco — halt ALL departments. Reason: CEO vacation, resuming [date].
```

When you return:
```
Run as /paco — resume ALL departments. Run standup and report what's pending.
```

---

Back to: [Getting Started](getting-started.md) | [Concepts](concepts.md) | [Adding Agents](adding-agents.md)
