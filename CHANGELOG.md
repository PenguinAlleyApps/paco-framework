# Changelog

All notable changes to PA·co Framework will be documented in this file.

## [2.2.0] — 2026-04-12 — v3 Architecture (Colossal Evolution)

### Added
- **6 new agents** (22 total): Scout (tool discovery), Discovery (client onboarding), Foreman (client builds), Watchman (hackathon monitoring), Pioneer (open source AI), Guardian (system guardrail)
- **3 new departments** (8 total): Consulting, Operations, plus Governance expanded with Harbor
- **Knowledge Graph** sections in all agent files — deterministic Layer 3 navigation map (UNTOUCHABLE rule)
- **Agent Cards** (`agents/cards/`) — JSON capability descriptors for A2A agent discovery
- **Constitutional AI** principles — 7 core principles for agent self-evaluation
- **Evaluation Framework** — LLM-as-Judge with dimensions for build/QA/spec/content output
- **Sunday Debate** schedule — weekly idea competition with 5-dimension scoring
- **Workflow as Code** pilot — consulting pipeline as executable state machine (`workflow-graph.py`)
- **Data Flywheel** — `operational_data` table captures agent failures, CEO corrections, lessons
- **Content Provenance** — metadata layer for all AI-generated content (model, prompt, timestamp, hash)
- **3 new modules**: Tools Warehouse, Open Source AI Solutions, Games (planning)
- **11 new wiki topic pages** for v3 modules
- **Interaction Failure Log** — 10 documented production failures with pattern taxonomy

### Changed
- **Weekly cycle**: eliminated Week A/B alternation → every week is identical (research + build + distribute)
- **Agent file limit**: 50 → 55 lines soft limit, with trim hierarchy (UNTOUCHABLE sections defined)
- **CLAUDE.md**: restructured from 151 → 128 lines with 22 lines headroom
- **Schedules**: 21 → 28 prompt files (Sunday Debate, Distribution Push, Weekly Build Plan, Research Accumulator, Hackathon Monitor, plus module schedules)

### Context
PA·co v3 transforms the system from "orchestration that helps build products" to "autonomous company operating system." The restructure was designed by Argus (external auditor) and executed across 5 phases. Phase 0 revealed the UNTOUCHABLE rule: Knowledge Graph sections must never be removed during optimization.

## [2.1.0] — 2026-04-01 — Schedule System

### Added
- **Schedule schema** (`core/schedule-schema.md`) — complete guide for time-triggered agent activations: work-hours schedules, 24/7 automation with smart skip logic, weekly maintenance, Build↔QA alternation pattern, Week A/B sprint cycle, and execution environment options (Claude Code scheduler, cron, GitHub Actions)

### Context
The v2 README promised "24/7 autonomous operations" and "19 schedules" but shipped no schedule documentation. This release fills that gap with battle-tested patterns from PA·co's own production schedule system.

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
