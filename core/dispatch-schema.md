# PA·co Dispatch System Schema

The dispatch system is how agents coordinate without stepping on each other. It's file-based, human-readable, and size-limited.

## Architecture

```
dispatch/
  GENERAL.md            — Cross-department. ALL agents read this.
  HALT.md               — Emergency stop. ALL agents read this FIRST.
  [department].md       — Department internal. Only that department reads/writes.
```

## HALT.md (always present)

```markdown
# Emergency Halt Register
## ONLY the CEO can add or remove halts.
## Every agent reads this FIRST, before anything else.
## If your department is HALTED: stop, log it, end session.

| Department | Status | Reason | Halted by | Date | Resume Date |
|---|---|---|---|---|---|
| [dept] | ACTIVE | — | — | — | — |
```

## GENERAL.md structure (max 120 lines)

```markdown
# General Dispatch

## Active Decisions
[Pricing, brand rules, standing directives — things ALL agents must respect]

## Cross-Department Handoffs
| Date | From | To | Action | Status | Verify By |
|------|------|----|--------|--------|-----------|

**Rule:** When marked DONE, originating department must VERIFY.

## CEO Updates
[Items the CEO communicated that affect everyone]
```

## Department dispatch structure (max 80 lines each)

```markdown
# [Department Name] Dispatch
## Agents: [list]
## Read this + dispatch/GENERAL.md at session start. Update both at session end.

## Also Monitor (read, don't write)
- `dispatch/[related-dept].md` — [why]

## Agent Health
| Agent | Last Heartbeat | Expected Freq | Status |
|-------|---------------|---------------|--------|

## Department State
- [Key metrics and current status]

## Pending Tasks
| Priority | Agent | Task | Source |
|----------|-------|------|--------|

## Activity Log (clears daily)
| Time | Agent | Action | Result |
|------|-------|--------|--------|
```

## Rules

1. **Every agent reads 2+ files at start:** HALT.md (first), GENERAL.md, their department dispatch, and any "Also Monitor" dispatches.
2. **Every agent updates 2 files at end:** GENERAL.md (if cross-department handoff) + their department dispatch (always).
3. **Cross-department items go in GENERAL.md only.** Never put a handoff for another department in your own dispatch.
4. **Intra-department items go in your dispatch only.** Don't clutter GENERAL with internal coordination.
5. **Size limits are hard constraints.** When approaching the limit, archive old entries. State files are current state, not historical logs.
6. **Activity logs clear daily.** Yesterday's work is history, not state.
7. **The CEO reads GENERAL.md.** Keep it crisp, actionable, and honest.

## Also Monitor — Cross-Department Subscriptions

Not every department is isolated. Some departments produce outputs that others NEED:

| Department | Should also read | Why |
|---|---|---|
| Engineering | quality-security, governance | See scan findings, catch legal/finance constraints |
| Quality & Security | engineering | Know what was deployed |
| Intelligence | growth, governance | Distribution data, pricing constraints |
| Growth | intelligence | Positioning changes, competitive angles |
| Governance | engineering | Detect new services that create cost/risk |
