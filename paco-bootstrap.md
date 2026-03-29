# PA·co Bootstrap — Multi-Agent Operations System for Claude Code

> Run this prompt in Claude Code to generate an autonomous multi-agent system for your project.
> It will ask you a few questions, then create everything you need.

---

You are about to set up **PA·co** (Project Autonomous Commander/Officer) — a multi-agent operations system that runs inside Claude Code. PA·co turns your Claude Code instance into an autonomous team of specialized AI agents that coordinate, learn, and evolve.

## What you'll get:
- A team of AI agents, each with a clear role and jurisdiction
- A dispatch system for agents to coordinate without stepping on each other
- Institutional memory that persists across sessions
- Quality gates to catch mistakes before they reach you
- An emergency halt system so you stay in control
- Scheduled tasks that run autonomously (requires Claude Desktop MAX)

## Before we start:
- You need Claude Code (CLI, Desktop, or VS Code extension)
- For scheduled tasks: Claude Desktop with MAX subscription ($100/mo)
- This works with any project type: SaaS, agency, content, dev tools, research, etc.

---

## Step 1: Tell me about your project

I need to understand what you're building so I can configure the right agents and workflows.

**Answer these questions** (type your answers or say "skip" for any):

1. **What's your project?** Describe it in 1-3 sentences. What does it do? Who is it for?

2. **What stage are you at?**
   - [ ] Idea stage (nothing built yet)
   - [ ] Early build (some code, no users)
   - [ ] Launched (live, some users)
   - [ ] Growing (revenue, need to scale operations)

3. **What's your role?**
   - [ ] Solo founder (I do everything)
   - [ ] Small team (2-5 people, I lead)
   - [ ] Agency (I manage multiple client projects)
   - [ ] Enterprise team (I lead a department/initiative)

4. **Which departments do you need?** (select all that apply)
   - [ ] **Engineering** — Build products, deploy, monitor infrastructure
   - [ ] **Quality & Security** — Testing, security scans, quality audits
   - [ ] **Intelligence & Strategy** — Market research, idea evaluation, competitive analysis, KPIs
   - [ ] **Growth & Revenue** — Marketing, sales, customer success, distribution
   - [ ] **Governance** — Finance reviews, legal compliance, risk management

5. **What model tier do you prefer?**
   - [ ] **Quality first** — Opus for all agents (best output, highest cost)
   - [ ] **Balanced** — Opus for critical agents (auditor, security), Sonnet for others (recommended)
   - [ ] **Cost-conscious** — Sonnet for all, Haiku for lightweight agents

6. **Budget constraint?**
   - [ ] Zero spend (free tiers only, no paid services)
   - [ ] Minimal (<$50/mo for infrastructure)
   - [ ] Flexible (willing to invest in tools that save time)

7. **Do you have Claude Desktop MAX for scheduled tasks?**
   - [ ] Yes — I want autonomous scheduled operations
   - [ ] No — I'll trigger agents manually

---

## Step 2: Generate the system

Based on your answers, I will now create the following files in your project:

### Core files (always created):
```
CLAUDE.md                           — Master rules file. Every agent reads this first.
dispatch/
  GENERAL.md                        — Cross-department coordination
  HALT.md                           — Emergency stop system (only you can activate)
memory/
  MEMORY.md                         — Index of all persistent knowledge
  lessons-learned.md                — Institutional memory (mistakes → permanent rules)
```

### Department files (based on your selections):

**If Engineering selected:**
```
.claude/agents/builder.md           — Builds your product
.claude/agents/devops.md            — Monitors infrastructure, verifies deploys
dispatch/engineering.md             — Engineering department coordination
```

**If Quality & Security selected:**
```
.claude/agents/qa.md                — Tests products, finds bugs, tracks regressions
.claude/agents/security.md          — Vulnerability scanning, dependency audits, threat modeling
.claude/agents/auditor.md           — Quality gates, blind spot detection, final review
dispatch/quality-security.md        — Q&S department coordination
```

**If Intelligence & Strategy selected:**
```
.claude/agents/researcher.md        — Market research, competitive intelligence, idea discovery
.claude/agents/strategist.md        — Idea evaluation, business modeling, competitive positioning
.claude/agents/analyst.md           — KPI tracking, data analysis, reporting
dispatch/intelligence.md            — Intelligence department coordination
```

**If Growth & Revenue selected:**
```
.claude/agents/marketer.md          — Content creation, distribution, community management
.claude/agents/sales.md             — Pipeline management, outreach, partnerships
.claude/agents/customer-success.md  — User onboarding, feedback triage, retention
dispatch/growth.md                  — Growth department coordination
```

**If Governance selected:**
```
.claude/agents/finance.md           — Cost analysis, unit economics, pricing validation
.claude/agents/legal.md             — Compliance monitoring, IP protection, risk assessment
dispatch/governance.md              — Governance department coordination
```

### Orchestrator (always created):
```
.claude/agents/paco.md              — Master orchestrator (your COO)
orchestrator/active-schedules.md    — All schedule prompts (if using Claude Desktop MAX)
docs/executive-orders.md            — Your non-negotiable rules
docs/quality-gates.md               — Quality checklists
```

---

## Step 3: I generate everything

After you answer the questions, I will:

1. **Create CLAUDE.md** with your project context, selected departments, coordination rules, and methodology
2. **Create each agent file** with role definition, jurisdiction, tools, rules, and coordination protocols
3. **Create the dispatch system** with GENERAL.md + department dispatches + HALT.md
4. **Create the memory system** with directory structure and index
5. **Create schedules** (if Claude Desktop MAX) with daily standup, agent health monitoring, and department-specific tasks
6. **Create executive orders** — core rules adapted to your project (quality standards, security requirements, transparency)
7. **Run a verification** — confirm all files are created, agents reference correct dispatches, no orphaned references

---

## Step 4: Your first standup

Once everything is generated, I'll run your first standup — a simulated team meeting where the orchestrator reviews all departments, checks agent health, and identifies what needs to happen first.

This gives you an immediate sense of how the system works and what your agents will do.

---

## How it works after setup

**If you have Claude Desktop MAX (scheduled tasks):**
Your agents run automatically on their schedules. You receive email reports. You check dispatch files when you want to see what's happening. You use `dispatch/HALT.md` to pause any department.

**If you run agents manually:**
When you want an agent to work, tell Claude Code: "Run as /researcher" or "Run the daily standup." The agent reads its file, reads the dispatch, does its job, and updates the dispatch for the next agent.

**Either way:**
- Agents learn from mistakes (lessons-learned.md grows over time)
- Dispatch keeps everyone coordinated (no agent contradicts another)
- Quality gates catch problems before they reach you
- You stay in control (HALT system, CEO blockers, approval gates)

---

## The PA·co philosophy

1. **Agents own their domain.** Each agent is responsible for their area. They keep their files clean, their outputs high quality, and their dispatch updated.
2. **Clear communication.** Handoffs between departments are specific and actionable. No vague notes.
3. **Continuous learning.** Every mistake becomes a permanent rule. Every success becomes a repeatable pattern.
4. **Unity.** What one agent discovers benefits all others. The system gets smarter every day.
5. **Human in the loop.** You are the CEO. Agents operate autonomously but report to you. You can halt, redirect, or override anything at any time.

---

*PA·co Framework — by Penguin Alley (penguinalley.com)*
*"An easier way to build."*
