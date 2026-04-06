# Migrating from AutoGen to PA·co Framework

AutoGen entered maintenance mode in early 2026 when Microsoft merged it into the Microsoft Agent Framework (combining AutoGen and Semantic Kernel). AutoGen standalone receives no new features, no security patches beyond critical CVEs, and no community investment.

If you built multi-agent systems on AutoGen, this guide maps AutoGen concepts to PA·co Framework equivalents and walks through a practical migration.

---

## Why AutoGen Teams Are Moving

Three things changed:

1. **No active development.** Microsoft Agent Framework RC 1.0 is the successor. AutoGen's GitHub shows no feature PRs since Q1 2026.
2. **Ecosystem fragmentation.** AutoGen users must choose: migrate to Microsoft Agent Framework (Semantic Kernel-based, Azure-centric) or switch to an independent framework.
3. **Claude Code maturity.** Claude Code now supports scheduled tasks, MCP servers, subagents API, and persistent file-based state — the infrastructure AutoGen users had to build manually.

PA·co Framework is the Claude Code-native alternative: zero-code, file-based, and designed for autonomous operations.

---

## Concept Mapping

| AutoGen Concept | PA·co Equivalent | Notes |
|----------------|------------------|-------|
| `AssistantAgent` / `UserProxyAgent` | Agent markdown file (`agents/builder.md`) | Define role, jurisdiction, and rules in markdown instead of Python classes |
| `GroupChat` | Department-based coordination | Agents coordinate through shared state files, not conversation threads |
| `GroupChatManager` | PA·co Orchestrator (CLAUDE.md) | The orchestrator reads PIPELINE.md and routes work to the right agent |
| System messages | `## I DO` / `## I DO NOT` sections | Behavioral boundaries defined declaratively |
| `register_function` | Claude Code native tools + MCP servers | No tool registration code — Claude Code tools are available by default |
| Conversation history | 4-layer Context Engineering | Identity + State + Relevant (pgvector) + Archive replaces flat message history |
| `is_termination_msg` | Quality gates + HALT system | Phase transitions replace termination conditions |
| Nested chats | Agent Teams (parallel execution) | 3-5 agents run in parallel via `playbooks/agent-teams.md` |
| `human_input_mode` | CEO Gate (phase 4) | Human approval is a mandatory workflow phase, not an optional parameter |

---

## Migration Steps

### Step 1: Map Your Agents

**AutoGen:**
```python
researcher = AssistantAgent(
    name="researcher",
    system_message="You research market trends...",
    llm_config={"model": "gpt-4"}
)
```

**PA·co:**
```markdown
# agents/researcher.md
---
name: "Researcher"
department: "intelligence"
model: "opus"
---
## I DO:
- Research market trends and competitive landscape
- Output structured SPEC_TEMPLATE files

## I DO NOT:
- Write code or deploy anything
- Make purchasing decisions
```

No Python. No API key management. Claude Code handles model selection and tool access.

### Step 2: Replace Group Chat with State Files

AutoGen coordinates agents through conversation threads. PA·co coordinates through files:

- **PIPELINE.md** — Which products exist and what phase they are in
- **STATE.md** (per product) — Current progress, last actor, remaining work
- **DISPATCH.md** (per product) — Cross-department handoffs and action items

Instead of agents talking to each other in a chat, each agent reads the current state, does its work, and updates the state file. The next agent reads the updated state.

### Step 3: Convert Workflows to the 7-Phase Lifecycle

AutoGen workflows are typically: define agents, start group chat, wait for termination condition. PA·co uses a structured lifecycle:

```
RESEARCH → REFINE → POST-REFINE → CEO GATE → DEVELOP → DEPLOY → EVOLVE
```

Map your AutoGen workflow stages to these phases. Most AutoGen projects map to:
- Agent planning conversations → **RESEARCH + REFINE**
- Agent execution conversations → **DEVELOP**
- Result verification → **POST-REFINE** (before build) or **QA review** (during build)

### Step 4: Set Up Persistent Knowledge

AutoGen keeps context in conversation history, which is lost between sessions. PA·co provides:

1. **State files** (markdown) — Current status, always up to date
2. **pgvector** (Supabase) — Semantic search over all historical knowledge
3. **RAG cache** — Pre-computed context for schedules that need speed

See [Context Engineering template](../templates/context-engineering/) for the pgvector setup.

### Step 5: Configure Scheduling

AutoGen requires external orchestration (cron jobs, Airflow, etc.) to run agents on schedule. PA·co uses Claude Code's built-in scheduled tasks:

```
# Example: Run builder every hour
Schedule: Hourly 24/7
Condition: product in DEVELOP + last_actor != "builder"
```

Schedules are defined in markdown and managed through Claude Code's task system. No external infrastructure needed.

---

## What You Gain

| Capability | AutoGen | PA·co Framework |
|-----------|---------|-----------------|
| Setup time | Hours (Python env, dependencies, API keys) | Minutes (bootstrap prompt) |
| Agent coordination | Code-based group chat | File-based state management |
| Persistent memory | Build it yourself | Built-in (pgvector + state files) |
| Human oversight | Optional `human_input_mode` | Mandatory CEO Gate + quality gates |
| Emergency stop | Kill the process | Edit HALT.md (instant, graceful) |
| 24/7 autonomous ops | External scheduler required | Built-in scheduled tasks |
| Debugging | Python debugger + logs | Read markdown files in any text editor |
| Cost | API costs + custom infra | Claude subscription only |

---

## What You Lose

PA·co is not a drop-in replacement for every AutoGen use case:

- **Multi-LLM support** — PA·co is Claude Code only. If you need GPT-4, Gemini, or local models, consider CrewAI or LangGraph.
- **Programmatic control** — If you need fine-grained Python control over agent execution, PA·co's markdown-first approach may feel limiting.
- **Runtime APIs** — AutoGen exposes Python APIs for dynamic agent creation. PA·co agents are defined in files at design time.

For users who were already using Claude with AutoGen, the migration is natural. For users deeply invested in multi-LLM or programmatic patterns, see [Comparisons](comparisons.md) for alternatives.

---

## Common Migration Questions

**Q: Can I migrate incrementally?**
Yes. Start by converting one AutoGen agent to a PA·co agent file and running it via Claude Code. Add more agents as you validate the approach.

**Q: What about my AutoGen tools?**
Claude Code provides native tools (Bash, Read, Write, Grep, Glob, Edit) plus MCP servers for external integrations. Most custom AutoGen tools map directly to MCP server implementations. See [MCP Transports](mcp-transports.md).

**Q: I used AutoGen's code execution sandbox. What replaces it?**
Claude Code executes code directly via the Bash tool with user-configured permission modes. For isolated execution, use the Subagents API with tool restrictions. See [Subagents](subagents.md).

**Q: How do I handle the Microsoft Agent Framework alternative?**
Microsoft Agent Framework is Azure-centric and requires Semantic Kernel. If you are not on Azure and prefer Claude, PA·co is a simpler path. If you are committed to Azure and multi-LLM, Microsoft Agent Framework may be the better choice.

---

Back to: [README](../README.md) | [Comparisons](comparisons.md) | [Getting Started](getting-started.md)
