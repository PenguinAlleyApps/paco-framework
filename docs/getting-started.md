# Getting Started with PA·co

Get your autonomous multi-agent system running in 10 minutes.

---

## Prerequisites

- **Claude Code** — CLI (`npm install -g @anthropic-ai/claude-code`), Desktop app, or VS Code extension
- **Claude account** — Any plan works for manual agent runs. Claude Desktop MAX ($100/mo) required for scheduled autonomous tasks.
- **Git** — to clone the framework

---

## Step 1: Clone the framework

```bash
# Into an existing project
cd your-project/
git clone https://github.com/penguin-alley/paco-framework .paco-framework --depth=1

# Or start fresh
git clone https://github.com/penguin-alley/paco-framework my-project
cd my-project
```

---

## Step 2: Run the bootstrap prompt

Open Claude Code (CLI or Desktop) in your project directory. Paste this prompt:

```
Read paco-bootstrap.md and execute the setup for my project.
```

Claude Code reads `paco-bootstrap.md` and asks you 5-7 questions.

---

## Step 3: Answer the setup questions

The bootstrap asks:

**1. What's your project?**
One to three sentences. What does it do, who is it for.

```
Example: "I'm building a SaaS for freelancers to generate branded invoices
in under 30 seconds. Target: designers and developers who hate billing admin."
```

**2. What stage are you at?**
Idea, early build, launched, or growing. This determines how many agents you need.

**3. What's your role?**
Solo founder, small team, agency, or enterprise. Determines the template used.

**4. Which departments do you need?**
Select the departments relevant to your stage:
- Engineering (always recommended)
- Quality & Security (add when you have something to protect)
- Intelligence & Strategy (add when you need market research or KPI tracking)
- Growth & Revenue (add when you're ready to acquire users)
- Governance (add when legal/finance becomes a real concern)

**5. Model preference?**
Balanced is the default (Opus for auditor/security, Sonnet for everything else). Cost-conscious (all Sonnet) works fine for early-stage.

**6. Do you have Claude Desktop MAX?**
If yes, you get scheduled tasks. If no, you trigger agents manually.

---

## Step 4: Verify the generated files

After answering, Claude Code generates your system. Verify these files exist:

```
CLAUDE.md                       ← Your master rules file
dispatch/
  HALT.md                       ← Emergency stop
  GENERAL.md                    ← Cross-department coordination
  engineering.md                ← (or your selected departments)
memory/
  MEMORY.md                     ← Knowledge index
  lessons-learned.md            ← Institutional memory (starts empty)
.claude/agents/
  paco.md                       ← Orchestrator
  builder.md                    ← (and other selected agents)
docs/
  executive-orders.md           ← Your non-negotiable rules
  quality-gates.md              ← Quality checklists
orchestrator/
  active-schedules.md           ← (if Claude Desktop MAX)
```

If any file is missing, tell Claude Code: "Verify the PA·co setup — check all required files exist."

---

## Step 5: Configure CLAUDE.md

Open `CLAUDE.md` and fill in the placeholders:

- `{{PROJECT_NAME}}` — your project name
- `{{CEO_NAME}}` — your name
- `{{MISSION}}` — one sentence: what you're building and for whom

The bootstrap fills these automatically, but verify they look right.

---

## Step 6: Run your first standup

In Claude Code:

```
Run as /paco — execute the daily standup.
```

The orchestrator will:
1. Read all dispatch files
2. Check agent health
3. Review pending tasks
4. Report what needs to happen next

This takes 1-2 minutes and gives you an immediate picture of your system state.

---

## Step 7: Trigger your first agent

Pick an agent and run it:

```
# Examples:
Run as /builder — check the build queue and start the next task.
Run as /researcher — scan for market opportunities in [your space].
Run as /marketer — create a launch post for [your product].
```

Each agent reads its file, reads the dispatch, does its job, and updates the dispatch for the next agent.

---

## Optional: Set up scheduled tasks (Claude Desktop MAX only)

If you have Claude Desktop MAX, `orchestrator/active-schedules.md` contains ready-to-paste schedule prompts. In Claude Desktop:

1. Open Settings > Scheduled Tasks
2. For each schedule in `active-schedules.md`, create a task with:
   - The prompt from that file
   - The frequency listed
   - Keep Awake: ON

The minimum useful set:
- Daily standup (9 AM)
- Build session (hourly)
- Weekly report (Friday 5 PM)

---

## What to expect in the first week

| Day | What happens |
|-----|-------------|
| Day 1 | Bootstrap complete. First standup. Agents oriented. |
| Day 2-3 | Builder starts first task. Dispatch fills with activity. |
| Day 4-5 | Mistakes happen. Agents log them to `lessons-learned.md`. |
| Day 7 | First weekly report. System starts feeling like a real team. |

---

## Common issues

**"Agent referenced a file that doesn't exist"**
Run: `Run as /paco — verify all agent references and fix broken paths.`

**"Two agents did the same work"**
Check jurisdiction sections in both agent files. One needs to explicitly cede that territory to the other. Update both files.

**"Agent keeps forgetting context from last session"**
Agents rely on dispatch files and memory files for context. Make sure the previous agent updated `dispatch/GENERAL.md` or the relevant department dispatch before ending its session.

**"I want to change how an agent behaves"**
Edit its file in `.claude/agents/`. Changes take effect next session. No restart needed.

---

Next: [Concepts](concepts.md) — understand how the pieces fit together.
