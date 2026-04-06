# Getting Started with PA·co

Get your autonomous multi-agent system running in 10 minutes.

---

## Prerequisites

- **Claude Code** — CLI (`npm install -g @anthropic-ai/claude-code`), Desktop app, VS Code, or JetBrains extension
- **Claude account** — Any plan works for manual agent runs. Claude MAX ($200/mo) required for scheduled autonomous tasks.
- **Git** — to clone the framework

---

## Step 1: Clone the framework

```bash
# Into an existing project
cd your-project/
git clone https://github.com/PenguinAlleyApps/paco-framework .paco-framework --depth=1

# Or start fresh
git clone https://github.com/PenguinAlleyApps/paco-framework my-project
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

**6. Do you have Claude MAX?**
If yes, you get scheduled tasks for autonomous operation. If no, you trigger agents manually.

---

## Step 4: Verify the generated files

After answering, Claude Code generates your system. Verify these files exist:

```
CLAUDE.md                       ← Master rules file (max 150 lines)
agents/
  paco.md                       ← Orchestrator agent
  builder.md                    ← (and other selected agents)
state/
  PIPELINE.md                   ← All products and their phases
  HALT.md                       ← Emergency stop register
  CEO_BLOCKERS.md               ← Items requiring your decision
products/
  _template/                    ← Template for new products
    CLAUDE.md                   ← Product-specific rules
    STATE.md                    ← Progress, bugs, last_actor
    DISPATCH.md                 ← Product task queue
catalogs/
  sectors.md                    ← Market sectors catalog
  tech-stacks.md                ← Technology references
specs/
  SPEC_TEMPLATE.md              ← Research output template
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
1. Read `state/PIPELINE.md` and all product STATE.md files
2. Check `state/HALT.md` (should be CLEAR)
3. Review `state/CEO_BLOCKERS.md` for items needing your decision
4. Report the current system state and what needs to happen next

---

## Step 7: Trigger your first agent

Pick an agent and run it:

```
# Examples:
Run as /builder — check the build queue and start the next task.
Run as /researcher — scan for market opportunities in [your space].
Run as /marketer — create a launch post for [your product].
```

Each agent reads its definition, checks the system state, does its job, and updates the relevant STATE.md for the next agent.

---

## Optional: Set up scheduled tasks (Claude MAX only)

If you have Claude MAX, create scheduled tasks in Claude Code for autonomous operation:

1. Open Claude Code settings or use the scheduled tasks feature
2. Create tasks for each schedule you need:
   - Daily standup (e.g., 8:00 AM)
   - Build session (hourly)
   - Weekly report (Friday 5 PM)

The minimum useful set:
- **Daily standup** — context sync, blocker identification
- **Build session** (hourly) — continuous development with Build/QA alternation
- **Weekly report** — CEO summary of the week

Each schedule reads `state/HALT.md` first. If halted, the agent exits silently.

---

## Optional: Add semantic memory with pgvector

When your system generates enough lessons and decisions that file-based memory becomes unwieldy, upgrade to vector-based retrieval. The [Context Engineering template](../templates/context-engineering/) includes:

- `schema.sql` — pgvector table, match function, and indexes for Supabase
- `pgvector-ingest.py` — parses markdown frontmatter, generates embeddings, inserts to Supabase
- `pgvector-search.py` — CLI semantic search with `--type`, `--scope`, and `--limit` filters

This is Layer 3 (Relevant) and Layer 4 (Archive) of the [4-layer Context Engineering](../core/context-engineering.md) system. Setup takes 5 minutes with a free Supabase project.

---

## What to expect in the first week

| Day | What happens |
|-----|-------------|
| Day 1 | Bootstrap complete. First standup. Agents oriented. |
| Day 2-3 | Builder starts first task. STATE.md fills with progress. |
| Day 4-5 | Build/QA alternation kicks in. Agents catch each other's gaps. |
| Day 7 | First weekly report. System starts feeling like a real team. |

---

## Common issues

**"Agent referenced a file that doesn't exist"**
Run: `Run as /paco — verify all agent references and fix broken paths.`

**"Two agents did the same work"**
Check jurisdiction sections in both agent files. One needs to explicitly cede that territory to the other. Update both files.

**"Agent keeps forgetting context from last session"**
Agents rely on STATE.md and PIPELINE.md for cross-session context (Layer 2: State). Make sure the previous agent updated `products/{name}/STATE.md` before ending its session. For deeper memory, set up pgvector (Layer 3: Relevant).

**"I want to change how an agent behaves"**
Edit its file in `agents/`. Changes take effect next session. No restart needed.

**"STATE.md or DISPATCH.md is getting too long"**
These files have hard line limits (STATE: 40 lines, DISPATCH: 100 lines). Archive completed items to vector DB or a lessons file, then rewrite with only current content.

---

Next: [Concepts](concepts.md) — understand how the pieces fit together.
