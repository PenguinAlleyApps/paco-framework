# Adding Agents

How to create a new agent and wire it into the system.

---

## When to add an agent

Add an agent when:
- A domain of work is growing beyond "one person can casually handle it"
- Two different agents are repeatedly doing the same type of task
- You find yourself manually doing something that could be systematized
- A new department emerges (legal concerns, a sales pipeline, customer feedback)

Don't add an agent for every small task. Agents are departments, not features. If the work is occasional and doesn't need specialized knowledge, the orchestrator or an existing agent can handle it.

---

## Step 1: Define the agent's identity

Before writing any file, answer these four questions:

**1. What is its singular job?**
One sentence. If you need two sentences, you have two agents.

```
Good: "The Researcher finds market opportunities and competitive intelligence."
Bad:  "The Researcher finds opportunities, evaluates them, writes the reports, and also helps with marketing."
```

**2. What does it explicitly NOT do?**
This is as important as what it does. List three to five things that an adjacent agent handles.

**3. How often does it run?**
Hourly, daily, weekly, or on-demand. This affects how you'll schedule it.

**4. What department does it belong to?**
Engineering, quality-security, intelligence, growth, or governance. If none fit, create a new department (and a new dispatch file).

---

## Step 2: Create the agent file

Create `.claude/agents/[name].md`. The name should be lowercase with hyphens: `customer-success.md`, `data-analyst.md`.

Use the schema from `core/agent-schema.md`:

```markdown
---
name: "Data Analyst"
description: "Tracks KPIs, builds dashboards, and produces the weekly business report"
model: "sonnet"
tools: ["Bash", "Read", "Write", "Glob", "Grep"]
maxTurns: 30
codename: "Prism"
department: "intelligence"
expected_frequency: "weekly"
---

> **Remember:** You are Claude Code. You have zero knowledge barriers.

You are the Data Analyst for [Project].

## MISSION
Turn raw data into decisions. Track KPIs, surface trends, and give the CEO
the numbers they need to steer the product.

## JURISDICTION

**I DO:**
- Pull metrics from Stripe API (revenue, MRR, churn)
- Pull usage data from Supabase (feature adoption, active users)
- Write the weekly business report
- Flag metric anomalies in GENERAL.md for CEO attention

**I DO NOT:**
- Write marketing content (that's /marketer)
- Make strategic decisions (that's /strategist)
- Fix broken tracking code (that's /builder)
- Monitor infrastructure uptime (that's /devops)

## PROCESS

1. Read `dispatch/HALT.md` — am I halted? If yes, stop here.
2. Read `dispatch/GENERAL.md` — active decisions affecting my work?
3. Read `dispatch/intelligence.md` — any queued analysis requests?
4. Pull data from sources (Stripe, Supabase, analytics)
5. Compare to prior week baseline in `memory/metrics-baseline.md`
6. Write report to `output/reports/metrics-YYYY-MM-DD.md`
7. Update `memory/metrics-baseline.md` with this week's numbers
8. If anomaly detected: add to `dispatch/GENERAL.md` → CEO attention
9. Update `dispatch/intelligence.md` with activity log

## RULES
1. Every metric must have a source URL or query — never fabricate numbers
2. Flag any metric that moved >20% week-over-week, positive or negative
3. Keep `memory/metrics-baseline.md` current — it's the baseline for next week
4. Reports go in `output/reports/` — never overwrite previous reports

## COORDINATION
- Reports to: orchestrator (/paco)
- Receives requests from: /strategist, /marketer (via intelligence dispatch)
- Hands off to: CEO (weekly report), /strategist (trend analysis)
```

---

## Step 3: Add agent health tracking to the department dispatch

Open `dispatch/[department].md` and add a row to the Agent Health table:

```markdown
## Agent Health
| Agent          | Last Heartbeat | Expected Freq | Status |
|----------------|----------------|---------------|--------|
| Researcher     | 2026-03-28     | daily         | OK     |
| Strategist     | 2026-03-28     | on-demand     | OK     |
| Data Analyst   | —              | weekly        | NEW    |  ← add this
```

---

## Step 4: Update CLAUDE.md

Open `CLAUDE.md` and add the new agent to the Agents section:

```markdown
## Agents
- /paco — Master orchestrator
- /builder — Engineering lead
- /researcher — Market intelligence
- /analyst — Data analysis + KPI tracking  ← add this
```

Also update the "What PA·co does" sections if this agent has any autonomous authority or reporting requirements.

---

## Step 5: Add to the orchestrator's standup

Open `.claude/agents/paco.md` and add the new agent to the daily standup check:

```markdown
## Daily Standup Process
For each agent, check:
- Last heartbeat vs expected frequency
- Any pending tasks in their dispatch
- Any GENERAL.md handoffs addressed to them

Agents to check:
- /builder (engineering.md)
- /devops (engineering.md)
- /researcher (intelligence.md)
- /analyst (intelligence.md)      ← add this
```

---

## Step 6: Create a schedule (if using Claude Desktop MAX)

Open `orchestrator/active-schedules.md` and add a schedule entry:

```markdown
## Data Analyst — Weekly (Fridays 4 PM)
**Tab:** Cowork
**Frequency:** Weekly, Fridays 4:00 PM

**Prompt:**
You are the Data Analyst (/analyst) for [Project]. Read
dispatch/HALT.md first, then dispatch/GENERAL.md, then
dispatch/intelligence.md. Pull this week's metrics from Stripe and
Supabase. Write the weekly report to output/reports/. Update the
baseline and dispatch files.
```

Then configure the task in Claude Desktop. See `orchestrator/active-schedules.md` for the exact steps.

---

## Step 7: Brief the orchestrator

Run a standup immediately after adding the agent:

```
Run as /paco — a new agent (/analyst) was just added to the intelligence
department. Run standup and orient the system.
```

The orchestrator reads the new agent file, verifies dispatch references are correct, and acknowledges the addition in its activity log.

---

## Examples: common agents to add

### Customer Success agent

When to add: you have users and are getting feedback/support requests.

```yaml
department: "growth"
expected_frequency: "daily"
```

Handles: user onboarding, feedback triage, support requests, churn detection.
Does NOT: make product decisions, write marketing copy, fix bugs.

### Sales agent

When to add: B2B outreach becomes a real focus.

```yaml
department: "growth"
expected_frequency: "daily"
tools_denied: ["Write"]  # Communicates via dispatch, doesn't edit source code
```

Handles: prospecting, outreach sequences, pipeline tracking, partnership conversations.
Does NOT: write blog content, code features, evaluate market trends.

### Legal agent

When to add: compliance concerns appear (GDPR, terms of service, IP questions).

```yaml
department: "governance"
expected_frequency: "weekly"
```

Handles: compliance monitoring, ToS reviews, IP checks, risk assessment.
Does NOT: write product code, market research, financial modeling.

### Security agent

When to add: you have a production product with real user data.

```yaml
department: "quality-security"
expected_frequency: "daily"
tools_denied: ["Write", "Edit"]  # Reports vulnerabilities, never patches them
```

Handles: vulnerability scanning, dependency audits, threat modeling, incident response.
Does NOT: fix the bugs it finds (reports to builder), write features.

---

## Mistakes to avoid

**Too broad a mandate.** "This agent handles all strategy" — no. Strategy is research + evaluation + positioning. Split it.

**Missing jurisdiction.** Every agent must say what it doesn't do. Without this, agents will duplicate work.

**No dispatch connection.** If an agent doesn't read and write to dispatch files, it's isolated. It will repeat work, miss context, and create conflicts.

**Wrong department.** Governance agents (legal, finance) should not write to engineering dispatch, and vice versa. Keep cross-department communication in GENERAL.md.

**Expecting agents to find their own tasks.** New agents need tasks assigned to them via dispatch before they'll do anything useful. Run a standup after adding a new agent so the orchestrator populates its queue.

**No tool restrictions.** Every agent should declare `tools_allowed` or `tools_denied`. An auditor that can edit the code it audits is a conflict of interest. A researcher with Write access could accidentally overwrite files. Use the tool whitelisting fields in the schema (`tools_allowed`, `tools_denied`) to enforce least privilege. See [core/agent-schema.md](../core/agent-schema.md) for patterns.

---

Next: [FAQ](faq.md) — common questions answered.
