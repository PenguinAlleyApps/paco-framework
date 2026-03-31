# Changelog

All notable changes to PA·co Framework will be documented in this file.

## [2.0.0] — 2026-03-31 — v2 Architecture Update

### Added
- **Context Engineering schema** (`core/context-engineering.md`) — 4-layer context system (Identity, State, Relevant, Archive) with pgvector support and file-based fallback
- **Workflow schema** (`core/workflow-schema.md`) — 7-phase product lifecycle (Research → Refine → Post-Refine → CEO Gate → Develop → Deploy → Evolve) with quality gates
- **State management schema** (`core/state-schema.md`) — product-centric state tracking with PIPELINE.md, per-product STATE.md, HALT.md, CEO_BLOCKERS.md, and Build↔QA alternation

### Changed
- **README** — rewritten to reflect v2 architecture: 7-phase workflow, 4-layer Context Engineering, state management, updated comparison table, revised battle-tested stats
- **Architecture** — evolved from dispatch-centric (v1) to product-centric state management (v2). v1 dispatch system preserved for simpler setups.

### Architecture (v2)
- 4-layer Context Engineering: Identity → State → Relevant → Archive
- 7-phase product workflow with quality gates per transition
- Product-centric coordination: `products/{name}/STATE.md` replaces department dispatches
- Global pipeline tracking: `state/PIPELINE.md`
- Optional vector DB (pgvector) for semantic knowledge retrieval (Layers 3-4)
- CEO Gate with 48h auto-approve and enhanced QA for autonomous builds
- Scheduled tasks: 19 schedules covering work hours + 24/7 automation + weekly reports

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
