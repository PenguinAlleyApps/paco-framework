# PA·co Framework vs CrewAI vs LangGraph vs AutoGen

A detailed comparison of multi-agent AI frameworks for developers and technical leaders evaluating their options.

---

## Overview

| Framework | Approach | Language | LLM Support | License | Status |
|-----------|----------|----------|-------------|---------|--------|
| **PA·co Framework** | Markdown-first, file-based coordination | None (markdown only) | Claude Code | MIT | Active (v2.0) |
| **CrewAI** | Python SDK with role-based agents | Python | Multi-LLM (OpenAI, Claude, Gemini, etc.) | Apache 2.0 | Active (v1.11+) |
| **LangGraph** | Python graph-based state machines | Python | Multi-LLM via LangChain | MIT | Active (v2.0) |
| **AutoGen** | Python group chat and nested agents | Python | Multi-LLM | MIT | Retired (maintenance mode) |

---

## Philosophy and Design

### PA·co Framework

PA·co treats multi-agent coordination as an **operations problem**, not a coding problem. Instead of writing Python to define agent behavior, you write markdown files that describe roles, workflows, and state. Claude Code reads these files and executes accordingly.

Key design principles:
- **Zero code**: Everything is markdown. No Python, no YAML configs, no infrastructure code.
- **Product lifecycle**: Agents exist to ship products through a 7-phase workflow, not just execute tasks.
- **Human governance**: CEO approval gates are built into the workflow. Agents operate autonomously within boundaries.
- **Context Engineering**: A 4-layer system (Identity, State, Relevant, Archive) ensures agents get the right information without context window bloat.

### CrewAI

CrewAI models agents as a **crew with roles and tasks**. You define agents in Python with backstories, goals, and tools, then assign them tasks that can be executed sequentially or in parallel.

Key design principles:
- **Role-based**: Each agent has a role, goal, and backstory that shapes its behavior.
- **Task-oriented**: Work is organized as discrete tasks assigned to specific agents.
- **Enterprise-ready**: Built for production use with monitoring, logging, and enterprise pricing tiers.
- **Multi-LLM**: Works with any LLM provider through a unified interface.

### LangGraph

LangGraph models agent workflows as **directed graphs**. Nodes represent agent actions, edges represent transitions, and state flows through the graph.

Key design principles:
- **Graph-based**: Workflows are explicit graphs with nodes and edges, giving fine-grained control.
- **State machines**: Built on state machine concepts with typed state objects.
- **Streaming-first**: Designed for real-time streaming of agent outputs.
- **Composable**: Graphs can be nested and composed for complex workflows.

### AutoGen (Retired)

AutoGen used **group chat** as its coordination metaphor. Agents talked to each other in conversations, with optional human participants.

Note: Microsoft retired AutoGen in early 2026, replacing it with the Microsoft Agent Framework. AutoGen remains available in maintenance mode but receives no new features.

---

## Feature Comparison

### Agent Definition

| Aspect | PA·co | CrewAI | LangGraph | AutoGen |
|--------|-------|--------|-----------|---------|
| **How agents are defined** | Markdown files with YAML frontmatter | Python classes with decorators | Python functions as graph nodes | Python classes inheriting from base |
| **Agent specialization** | I DO / I DO NOT sections in markdown | Role, goal, backstory parameters | Custom logic per node function | System messages per agent |
| **Department organization** | Built-in (Engineering, QA, etc.) | Manual grouping | No concept | No concept |
| **Agent count** | 3-16 recommended | No hard limit | No hard limit | No hard limit |

**PA·co example:**
```yaml
---
name: "Builder"
department: "engineering"
---
## I DO:
- Write code from specifications
## I DO NOT:
- Create marketing content
```

**CrewAI example:**
```python
researcher = Agent(
    role="Senior Researcher",
    goal="Find market opportunities",
    backstory="Expert analyst...",
    tools=[search_tool]
)
```

**LangGraph example:**
```python
def research_node(state):
    result = llm.invoke(state["query"])
    return {"research": result}

graph.add_node("research", research_node)
```

### Workflow Management

| Aspect | PA·co | CrewAI | LangGraph | AutoGen |
|--------|-------|--------|-----------|---------|
| **Workflow type** | 7-phase product lifecycle | Sequential or parallel tasks | Directed graph with conditional edges | Conversation flow |
| **Phase transitions** | Quality gates with gatekeeper agents | Task completion triggers | Conditional edge functions | Chat termination conditions |
| **Product lifecycle** | Built-in (Research through Evolve) | None | None | None |
| **Human approval** | CEO Gate (mandatory phase) | None built-in | Interrupt points (manual setup) | Human proxy agent |

PA·co is the only framework that treats the **product lifecycle** as a first-class concept. Other frameworks handle task execution but do not model the journey from idea to shipped product.

### Context and Memory

| Aspect | PA·co | CrewAI | LangGraph | AutoGen |
|--------|-------|--------|-----------|---------|
| **Context system** | 4-layer Context Engineering | In-memory per session | State dictionary | Message history |
| **Knowledge persistence** | pgvector + markdown files | Optional RAG integration | None built-in | None built-in |
| **Cross-session memory** | Automatic (vector DB + state files) | Manual implementation | Manual implementation | Manual implementation |
| **Context optimization** | Layers filter what each agent sees | All context in prompt | State pruning via code | Full conversation history |

PA·co's 4-layer Context Engineering is purpose-built for multi-agent systems where different agents need different information:

1. **Identity**: Who am I? (agent definition, org rules)
2. **State**: What is happening now? (product progress, pipeline status)
3. **Relevant**: What do I need to know? (semantic search from vector DB)
4. **Archive**: Everything else (available if queries change)

### Safety and Control

| Aspect | PA·co | CrewAI | LangGraph | AutoGen |
|--------|-------|--------|-----------|---------|
| **Emergency stop** | HALT.md (instant, global) | None | None | None |
| **Spending control** | CEO approval required (EO-005) | None | None | None |
| **Quality gates** | Every phase transition | None | None | None |
| **Audit trail** | STATE.md + DISPATCH.md per product | Logging (optional) | State snapshots | Chat history |
| **Build/QA alternation** | Enforced via last_actor | None | None | None |

### Setup and Learning Curve

| Aspect | PA·co | CrewAI | LangGraph | AutoGen |
|--------|-------|--------|-----------|---------|
| **Time to first agent** | 5 minutes (bootstrap prompt) | 30-60 minutes (Python setup + code) | 1-2 hours (graph concepts + code) | 30-60 minutes (Python setup + code) |
| **Prerequisites** | Claude Code installed | Python, pip, API keys | Python, pip, LangChain knowledge | Python, pip, API keys |
| **Configuration** | Edit markdown files | Edit Python code | Edit Python code | Edit Python code |
| **Debugging** | Read state files in any text editor | Python debugger + logging | Python debugger + LangSmith | Python debugger + logging |

### Pricing and Cost Model

| Framework | Framework cost | Runtime cost | Enterprise tier |
|-----------|---------------|-------------|-----------------|
| **PA·co** | $0 (MIT) | Claude subscription ($20-200/mo) | Premium templates ($49-249) |
| **CrewAI** | Free (open source) | API costs + CrewAI Plus ($99/mo) | CrewAI Enterprise ($120K+/year) |
| **LangGraph** | Free (open source) | API costs + LangSmith ($39/user/mo + $0.001/node) | LangSmith Enterprise (custom) |
| **AutoGen** | Free (MIT, retired) | API costs only | None (retired) |

---

## Decision Guide

### Choose PA·co Framework if:

- You use Claude Code and want multi-agent operations without writing code
- You need a structured product lifecycle (not just task execution)
- You want human-in-the-loop governance built into the workflow
- You are a solo founder or small team wanting autonomous 24/7 operations
- You value simplicity: markdown files over Python codebases
- You want knowledge persistence across sessions without building it yourself

### Choose CrewAI if:

- You need multi-LLM support (OpenAI, Claude, Gemini, local models)
- Your team has Python expertise and prefers code-based configuration
- You need enterprise support and SLAs
- You want a large community (20K+ GitHub stars) and ecosystem
- You are building task-oriented workflows, not product lifecycles

### Choose LangGraph if:

- You need fine-grained control over agent execution flow
- You are building complex, branching workflows with conditional logic
- You want real-time streaming of agent outputs
- You are already in the LangChain ecosystem
- You need graph visualization of your agent workflows

### Choose a custom solution if:

- You need to use models other than Claude and need more control than CrewAI provides
- Your use case does not fit the multi-agent pattern (single agent is sufficient)
- You are building a framework, not using one

---

## Migration Paths

### From AutoGen to PA·co

AutoGen was retired by Microsoft in early 2026. If you are migrating:

1. Map your AutoGen agents to PA·co agent markdown files
2. Replace group chat coordination with PA·co state management
3. Convert conversation-based workflows to the 7-phase product lifecycle
4. Move any persistent state to PA·co STATE.md files
5. Set up pgvector for knowledge that was previously in message history

### From CrewAI to PA·co

1. Convert Python agent definitions to markdown files
2. Map CrewAI tasks to PA·co workflow phases
3. Replace CrewAI tools with Claude Code native tools (Bash, Read, Write, Grep, etc.)
4. Set up state management (PIPELINE.md, STATE.md per product)
5. Configure scheduled tasks to replace manual triggering

---

## Frequently Asked Questions

### Can PA·co work with models other than Claude?

No. PA·co Framework is built specifically for Claude Code. The agent file format, tool access, and scheduling system are Claude Code features. For multi-LLM support, consider CrewAI or LangGraph.

### Is PA·co suitable for enterprise use?

PA·co is designed for solo founders and small teams (1-10 people). It has strong governance features (CEO Gate, quality gates, emergency halt) but does not have enterprise features like SSO, audit logging to external systems, or SLA guarantees. For enterprise needs with dedicated support, consider CrewAI Enterprise.

### Can I use PA·co and CrewAI together?

Technically possible but not recommended. They solve the same problem (multi-agent coordination) with fundamentally different approaches. Pick one and commit to it.

### How does PA·co handle errors differently?

PA·co has three layers of error defense:
1. **Quality gates** catch issues before they reach production
2. **Build/QA alternation** ensures every build is reviewed
3. **HALT system** provides instant emergency stop

Other frameworks rely on try/catch in Python code and manual error handling.

---

Back to: [README](../README.md) | [FAQ](faq.md) | [Getting Started](getting-started.md)
