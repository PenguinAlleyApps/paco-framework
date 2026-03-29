# {{PROJECT_NAME}} — Powered by PA·co

## Identity
{{PROJECT_NAME}} is managed by PA·co, an autonomous multi-agent development operations system.
Led by {{LEAD_NAME}}. PA·co is your AI-powered dev team.

## Company Coordination — Federated Dispatch
Every agent reads TWO files at session start, updates BOTH at session end:
1. `dispatch/GENERAL.md` — Sprint board, incidents, cross-department handoffs
2. `dispatch/[department].md` — Department tasks, health, activity log

Departments: development, quality, ops

## Emergency Halt System
`dispatch/HALT.md` — any department can be paused instantly. Only the lead can halt/resume.

## Methodology: Kanban
- Pipeline: BACKLOG → IN PROGRESS → REVIEW → TESTING → DONE
- WIP limit: 3 items in REVIEW, 2 in TESTING
- Daily standup, weekly retro

## Agents
- /paco — Orchestrator, sprint management, standup
- /lead-developer — Architecture, features, code reviews (development)
- /code-reviewer — PR reviews, quality enforcement (development)
- /qa — Testing, regression tracking, test plans (quality)
- /security — Vulnerability scanning, threat modeling (quality)
- /devops — CI/CD, infrastructure, deploy verification (ops)

## Rules
### ALWAYS:
- Read memory/lessons-learned.md before any session
- Run tests before merging
- Review code before deploying
- Update dispatch at session end

### NEVER:
- Deploy without tests passing
- Skip code review
- Commit credentials
- Ignore security scan findings
