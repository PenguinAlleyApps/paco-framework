# Agent-to-Agent (A2A) Coordination in PA·co

How PA·co agents communicate, delegate, and coordinate work without runtime message passing.

---

## The problem A2A solves

When you have multiple agents, they need to coordinate. Who works on what? How does Agent A tell Agent B that a task is ready? How do you prevent two agents from doing the same thing?

The industry calls this **Agent-to-Agent (A2A) coordination**. Google formalized it as a protocol in 2025, and by 2026 it's table stakes -- CrewAI, Google ADK, and others ship A2A support natively.

PA·co solves the same problem with a fundamentally different approach.

---

## Two approaches to A2A

### Runtime message passing (CrewAI, Google ADK)

Agents exchange messages through an API at runtime. Agent A sends a structured message to Agent B, waits for a response, and acts on it. This requires:

- A running process or server for each agent
- A message broker or direct API connection
- Schema definitions for message formats
- Error handling for unavailable agents
- Session management for multi-turn conversations

### File-based coordination (PA·co)

Agents coordinate through shared markdown files. Agent A writes to a dispatch file; Agent B reads it at its next session start. No running processes, no APIs, no message broker.

```
Agent A (Builder)                    Agent B (QA)
    |                                    |
    |-- writes STATE.md -------->        |
    |   last_actor: "builder"            |
    |                                    |
    |                            reads STATE.md
    |                            sees: last_actor = "builder"
    |                            knows: my turn to review
    |                                    |
    |                            writes STATE.md
    |                            last_actor: "qa"
    |                                    |
    |<-------- reads STATE.md --|
    |   sees: last_actor = "qa"
    |   knows: my turn to build
```

This is A2A coordination without runtime infrastructure.

---

## PA·co's A2A patterns

### Pattern 1: Turn-based alternation

The simplest coordination pattern. Two agents take turns via a shared state flag.

**Use case:** Build/QA cycles, review loops, any ping-pong workflow.

**How it works:**

```yaml
# In products/{name}/STATE.md
last_actor: "builder"   # QA runs next
last_actor: "qa"        # Builder runs next
last_actor: "none"      # Either can run
```

Each agent checks `last_actor` at session start. If it's their turn, they work. If not, they skip silently.

**Why this works:** Claude Code sessions are discrete. There's no "waiting" -- agents simply check state at their next scheduled run.

### Pattern 2: Cross-department handoff

When work crosses department boundaries (e.g., Engineering to Growth), agents write to a shared dispatch file.

**Use case:** "Product deployed, create launch content" or "Security issue found, halt engineering."

**How it works:**

```markdown
# In dispatch/GENERAL.md or state/PIPELINE.md

## Cross-Department Handoffs
| Date       | From      | To        | Action                           | Status  |
|------------|-----------|-----------|----------------------------------|---------|
| 2026-04-04 | Builder   | Marketer  | Compliora v2.1 LIVE — launch post | PENDING |
| 2026-04-04 | Auditor   | Builder   | Fix SEC-001 before deploy         | PENDING |
```

The receiving agent reads this file at session start and picks up pending work.

### Pattern 3: Escalation chain

When an agent encounters something outside its jurisdiction, it escalates through a defined path.

**Use case:** Builder finds a security issue, QA finds a business logic question, any agent hits a CEO blocker.

**How it works:**

```
Agent → Department dispatch → GENERAL.md → CEO_BLOCKERS.md
  (internal)   (cross-dept)     (human escalation)
```

Each level has clear criteria for when to escalate further:

| Level | File | When to use |
|-------|------|-------------|
| Internal | `dispatch/{dept}.md` | Stays within the department |
| Cross-department | `dispatch/GENERAL.md` | Another department needs to act |
| Human escalation | `state/CEO_BLOCKERS.md` | Requires human decision or approval |

### Pattern 4: Pipeline phase gates

Agents coordinate through phase transitions in the product pipeline. Each phase has a defined set of agents that participate.

**Use case:** Moving a product from Research to Refine to Deploy.

**How it works:**

```yaml
# In state/PIPELINE.md
| Product   | Phase    | Status                    |
|-----------|----------|---------------------------|
| MyApp     | DEVELOP  | Builder working on auth    |
```

Phase transitions are the coordination mechanism:

```
RESEARCH (Researcher)
    ↓ gate: spec exists
REFINE (ALL departments in parallel)
    ↓ gate: auditor approval
CEO GATE (human approval)
    ↓ gate: CEO says GO
DEVELOP (Builder ↔ QA alternation)
    ↓ gate: all specs implemented, QA pass
DEPLOY (Builder + QA + Security)
    ↓ gate: health checks pass
EVOLVE (all agents, continuous)
```

Each agent knows which phases it participates in. The pipeline file is the single source of truth for what phase each product is in.

### Pattern 5: Priority override

Critical issues override normal turn-based coordination.

**Use case:** P0 bug found in production, security vulnerability discovered.

**How it works:**

```yaml
# P0 bugs override last_actor
# Any agent seeing a P0 bug acts immediately regardless of turn
bugs_active: 1
bug_priority: P0
```

The rule is simple: P0/P1 bugs in any product always take priority over normal work. Every agent checks for active bugs before checking whose turn it is.

---

## Comparison with runtime A2A protocols

| Aspect | Runtime A2A (Google, CrewAI) | PA·co file-based A2A |
|--------|------|------|
| **Transport** | HTTP/gRPC messages | File reads/writes |
| **Latency** | Milliseconds (real-time) | Minutes to hours (schedule-based) |
| **Infrastructure** | Servers, message brokers | Filesystem (git repo) |
| **Agent discovery** | Service registry / agent cards | Agent schema files in `.claude/agents/` |
| **State persistence** | Database or in-memory | Markdown files (versioned in git) |
| **Failure handling** | Retry logic, circuit breakers | Next scheduled run picks up where it left off |
| **Audit trail** | Logs, traces | Git history (every state change is a commit) |
| **Scalability** | Horizontal (more servers) | Vertical (more scheduled sessions) |

### When PA·co's approach is better

- **Solo developers or small teams** who don't want to maintain infrastructure
- **Claude Code-native workflows** where agents are Claude Code sessions, not microservices
- **Auditability requirements** where git history provides a complete coordination trail
- **Simplicity** -- no message schemas, no serialization, no network errors

### When runtime A2A is better

- **Sub-second coordination** where agents must react in real time
- **Cross-platform agents** that span multiple LLM providers or tools
- **High-throughput systems** processing thousands of agent interactions per minute
- **Multi-tenant platforms** where agents serve different users simultaneously

---

## Implementing A2A in your PA·co system

### Step 1: Define agent jurisdictions

Every agent needs clear boundaries. If two agents can both do "marketing," you have a coordination problem. See [Agent Schema](../core/agent-schema.md) for the jurisdiction pattern.

### Step 2: Choose your coordination pattern

| Situation | Pattern | Files involved |
|-----------|---------|----------------|
| Two agents taking turns | Turn-based alternation | `STATE.md` (`last_actor`) |
| Work crossing departments | Cross-department handoff | `dispatch/GENERAL.md` |
| Something needs human input | Escalation chain | `CEO_BLOCKERS.md` |
| Product moving through phases | Pipeline phase gates | `PIPELINE.md` |
| Critical issue overrides normal flow | Priority override | `STATE.md` (`bugs_active`) |

### Step 3: Set up state files

Each coordination pattern uses specific files. Create them from the schemas in `core/`:

- [`state-schema.md`](../core/state-schema.md) -- product state including `last_actor`
- [`dispatch-schema.md`](../core/dispatch-schema.md) -- cross-agent communication
- [`workflow-schema.md`](../core/workflow-schema.md) -- phase transitions

### Step 4: Schedule your agents

Coordination only works if agents run on a schedule. Use Claude Code scheduled tasks or cron jobs to trigger agent sessions at defined intervals.

```
Builder:    Every hour
QA:         Every hour (alternates with Builder via last_actor)
Researcher: Daily at 7:30 AM
Auditor:    After phase transitions
```

---

## FAQ

**Q: Can PA·co agents talk to each other in real time?**
No. PA·co uses asynchronous, file-based coordination. Agents read state at session start and write state at session end. There's no real-time messaging. This is a deliberate design choice -- it's simpler, more auditable, and doesn't require infrastructure.

**Q: How do I integrate with external A2A-compatible agents?**
If you need to coordinate with agents running on CrewAI, LangGraph, or other runtime frameworks, build a bridge agent that reads their outputs (via API) and writes to PA·co dispatch files. The bridge translates between runtime messages and file-based state.

**Q: What happens if two agents write to the same file at the same time?**
In Claude Code, sessions are sequential within a single instance. If you run multiple Claude Code instances, use git's conflict resolution. The scheduling system (hourly runs with `last_actor` checks) is designed to prevent concurrent writes.

**Q: Is PA·co's approach compatible with Google's A2A protocol?**
They solve the same problem differently. PA·co's file-based coordination is functionally equivalent to A2A's task lifecycle (pending → running → completed) -- the state transitions just happen in markdown files instead of API calls. If you need formal A2A protocol compliance for interoperability, build the bridge agent described above.

---

Next: [Comparisons](comparisons.md) -- see how PA·co stacks up against CrewAI, LangGraph, and AutoGen.
