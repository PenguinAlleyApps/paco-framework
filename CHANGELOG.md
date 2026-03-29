# Changelog

All notable changes to PA·co Framework will be documented in this file.

## [0.1.0] — 2026-03-29 — Initial Release

### Added
- **Bootstrap prompt** (`paco-bootstrap.md`) — generates entire PA·co system from 7 questions
- **Solo-founder template** — 4 agents (orchestrator, builder, devops, marketer), 2 departments (engineering, growth)
- **Startup template** — 8 agents (+ QA, researcher, strategist, sales), 5 departments with cross-department subscriptions
- **Core schemas** — agent, dispatch, memory, and executive orders templates
- **Dispatch system** — federated coordination with GENERAL.md + department dispatches + HALT emergency stop
- **Memory system** — file-based institutional knowledge with lessons-learned pattern
- **Quality gates** — universal pre-deploy, pre-launch, content, and research checklists
- **Documentation** — getting-started, concepts, adding-agents, FAQ
- **Case study** — how PA·co built and operates Penguin Alley (7 products, 16 agents)
- **MIT License**
- **Contributing guide** with template submission process

### Architecture
- Markdown-first: all configuration in .md files, zero code required
- Claude Code native: designed specifically for Claude Code (CLI, Desktop, VS Code)
- File-based state: dispatch/ for coordination, memory/ for persistence
- Department isolation: agents read only their department + GENERAL
- Emergency halt: CEO can pause any department via HALT.md
