# Schedule Schema

Schedules are time-triggered agent activations that run autonomously. They are the backbone of 24/7 operations — the system works while you sleep.

## Schedule File Structure

Each schedule lives in `scripts/schedules/{name}.md`:

```markdown
# Schedule: {Name} — {Frequency} ({Tab/Runner})

HALT CHECK: Read state/HALT.md. If HALT ALL or HALT [{product}] is active, exit immediately.
CEO BLOCKERS: Read state/CEO_BLOCKERS.md. If you generate a CEO blocker, add it there.
You are PA·co's {Department} team ({Agent1} + {Agent2}).
Read CLAUDE.md, agents/{agent1}.md, agents/{agent2}.md.

{SCHEDULE NAME} — {frequency description}.

SKIP if {skip condition}.

{Numbered steps — what the agent does each run.}

Update state/DISPATCH_TODAY.md. Git commit + push.
```

## Schedule Types

### Work-Hours Schedules
Run during business hours (e.g., 7 AM - 2 PM). Best for tasks that need human oversight the same day.

```yaml
type: work_hours
examples:
  - name: TechMonitor
    when: "7:00 AM daily"
    condition: Always
    agents: [Researcher]
    purpose: Capture industry news, tag by sector

  - name: Standup
    when: "8:00 AM daily"
    condition: Always
    agents: [Orchestrator]
    purpose: Context sync, knowledge sharing, CEO feedback routing

  - name: Refine
    when: "8:30-10:30 AM daily (staggered by department)"
    condition: "If SPEC_TEMPLATE exists today + Week A"
    agents: [All departments in parallel]
    purpose: Enrich specs with department expertise
```

### 24/7 Automation Schedules
Run around the clock. Must have **smart skip logic** to avoid wasted runs.

```yaml
type: always_on
examples:
  - name: Build Session
    when: "Hourly 24/7"
    condition: "product in APPROVED/DEVELOP + last_actor != builder"
    agents: [Builder]
    purpose: Build from specs. Never improvise.

  - name: QA Review
    when: "Hourly 24/7"
    condition: "product in DEVELOP + last_actor = builder"
    agents: [QA, Security]
    purpose: Verify builds. Build/QA alternation via last_actor.

  - name: Content Creation
    when: "Hourly 9AM-11PM"
    condition: "Smart skip - cycle through create/visual/publish/engage"
    agents: [Marketer]
    purpose: Content pipeline with state tracking
```

### Weekly Schedules
Run once per week for reporting and maintenance.

```yaml
type: weekly
examples:
  - name: Weekly Report
    when: "Friday 5:00 PM"
    condition: Always
    agents: [Orchestrator]
    purpose: CEO summary + context health audit

  - name: Open Source Sync
    when: "Friday 6:00 PM"
    condition: "If OSS products in Evolve"
    agents: [Marketer, Builder]
    purpose: Internal to public repo sync, community response
```

## Smart Skip Logic

Every 24/7 schedule must define conditions that prevent wasted runs:

```markdown
## Skip Conditions (check BEFORE doing work)

1. **State-based skip:** Check last_actor in STATE.md. If it is your turn, run. Otherwise, skip.
2. **Tracker-based skip:** Check tracker file. If all actions for this cycle are done, skip.
3. **Time-based skip:** Check last_completed timestamp. If too recent, skip.
4. **Content-based skip:** Check if there is actually work to do (drafts to publish, leads to follow up).
```

Example - Content Creation smart skip:
```
Read CONTENT_TRACKER.md
Determine current cycle position: CREATE -> VISUAL -> PUBLISH -> ENGAGE
If current action already done today -> skip
If no drafts exist and action = PUBLISH -> skip
Otherwise -> execute current action, advance cycle position
```

## Build/QA Alternation

The most important coordination pattern. Prevents builders from overwriting QA findings and vice versa.

```
STATE.md contains: last_actor: "builder" | "qa"

Build Session checks: if last_actor = "builder" -> SKIP (QA has not reviewed yet)
QA Session checks: if last_actor = "qa" -> SKIP (Builder has not built yet)

After Build completes: set last_actor = "builder"
After QA completes: set last_actor = "qa"
```

## Week A/B Sprint Cycle

Alternating focus prevents context-switching waste:

```
Week A = SPRINT (produce - build, ship, create)
Week B = CONSOLIDATE (position - distribute, improve, engage)

Schedules 4-9 (Refine pipeline) skip in Week B.
Distribution/content schedules run in both but shift emphasis.
```

Track in PIPELINE.md:
```markdown
## Current Week Mode
- mode: SPRINT | CONSOLIDATE
- week_start: YYYY-MM-DD
- next_switch: YYYY-MM-DD
```

## Registering Schedules

List all schedules in CLAUDE.md so every agent knows the full picture:

```markdown
## Schedules
| # | Schedule | When | Condition |
|---|---|---|---|
| 1 | TechMonitor | 7:00 AM daily | Always |
| 2 | Build Session | Hourly 24/7 | product in DEVELOP + last_actor != builder |
| ... | ... | ... | ... |
```

## Execution Environment

Schedules are triggered by your CI/CD system, cron, or Claude Code's built-in scheduler. The schedule file is the **prompt** — it tells the agent what to do. The environment just triggers it at the right time.

Options:
- **Claude Code scheduled tasks** — built-in, simplest setup
- **Cron + CLI** — `0 * * * * claude-code run scripts/schedules/build.md`
- **GitHub Actions** — scheduled workflows that invoke Claude Code
- **Custom orchestrator** — any system that can run prompts on a schedule

---

*Built by PA·co — A Penguin Alley System*
*https://penguinalley.com*
