# Subagents API Integration

How to spawn PA·co agents programmatically using the Anthropic Claude Agent SDK.

---

## Why subagents matter for PA·co

PA·co agents are defined as markdown files. The Claude Agent SDK lets you spawn those same agents programmatically with isolated contexts, restricted tools, and parallel execution. This gives you two ways to run PA·co:

| Approach | Best for | How it works |
|----------|----------|--------------|
| **File-based** (default) | Claude Code sessions, scheduled tasks | Agent reads `.claude/agents/[name].md` at session start |
| **SDK subagents** | Custom applications, CI/CD, API integrations | Your code spawns agents via `query()` with `AgentDefinition` |

Both approaches use the same agent design principles (jurisdiction, tool restrictions, coordination). The SDK approach adds programmatic control over when and how agents run.

---

## Mapping PA·co agents to SDK subagents

Every PA·co agent schema field maps directly to a Claude Agent SDK `AgentDefinition` field:

| PA·co agent schema | SDK `AgentDefinition` | Notes |
|--------------------|----------------------|-------|
| `name` | key in `agents` dict | `"builder"`, `"auditor"`, etc. |
| `description` | `description` | SDK uses this to decide when to invoke the agent |
| Agent body (markdown) | `prompt` | The full agent instructions |
| `model` | `model` | `"opus"`, `"sonnet"`, `"haiku"` |
| `tools` | `tools` | If omitted, inherits all parent tools |
| `tools_allowed` | `tools` | In SDK, use `tools` as whitelist directly |
| `tools_denied` | (not in SDK) | Apply deny logic before passing to `tools` |

### Converting `tools_allowed` / `tools_denied` to SDK `tools`

PA·co's three-field resolution (`tools`, `tools_allowed`, `tools_denied`) collapses to a single `tools` array in the SDK:

```python
def resolve_tools(agent_schema: dict) -> list[str]:
    """Convert PA·co tool fields to SDK tools array."""
    allowed = agent_schema.get("tools_allowed", [])
    denied = set(agent_schema.get("tools_denied", []))

    if allowed:
        base = allowed
    else:
        base = agent_schema.get("tools", [])

    return [t for t in base if t not in denied]
```

---

## Example: PA·co department as SDK subagents

This example creates a PA·co-style build session with Builder and QA agents as SDK subagents. The orchestrator spawns both and coordinates their work.

### Python

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition


BUILDER_PROMPT = """You are the Builder for this project.

## MISSION
Write code and ship products.

## JURISDICTION
I DO: write code, run migrations, deploy, debug
I DO NOT: write marketing copy, evaluate ideas, run security audits

## PROCESS
1. Read the product STATE.md for current progress
2. Read mvp-specs/ for what to build
3. Build the next piece according to specs
4. Update STATE.md with progress

## RULES
- Never commit secrets to git
- Test before deploying
- Follow existing code patterns
"""

QA_PROMPT = """You are the QA Reviewer for this project.

## MISSION
Verify code quality, security, and spec compliance.

## JURISDICTION
I DO: run tests, review code, scan for vulnerabilities, verify specs
I DO NOT: write features, fix bugs, deploy to production

## PROCESS
1. Read STATE.md — what did the builder change?
2. Run the test suite
3. Check for security issues (exposed secrets, missing auth, SQL injection)
4. Verify changes match the spec
5. Write QA result to STATE.md

## RULES
- Never modify source code — report issues only
- Every finding needs: severity, location, description, fix suggestion
- PASS or FAIL — no "partial pass"
"""


async def build_session(product_path: str):
    """Run a PA·co build+QA session using SDK subagents."""
    async for message in query(
        prompt=f"""Run a build session for the product at {product_path}.

1. Use the builder agent to implement the next item from mvp-specs/
2. After the builder finishes, use the qa-reviewer agent to verify the work
3. Report the combined results.""",
        options=ClaudeAgentOptions(
            allowed_tools=[
                "Read", "Edit", "Write", "Bash",
                "Glob", "Grep", "Agent",
            ],
            agents={
                "builder": AgentDefinition(
                    description="Builds product features from specs. Use for all code implementation tasks.",
                    prompt=BUILDER_PROMPT,
                    tools=["Read", "Edit", "Write", "Bash", "Glob", "Grep"],
                    model="sonnet",
                ),
                "qa-reviewer": AgentDefinition(
                    description="Reviews code for quality and security. Use after builder completes work.",
                    prompt=QA_PROMPT,
                    # Read-only + Bash for running tests — no Edit or Write
                    tools=["Read", "Bash", "Glob", "Grep"],
                    model="sonnet",
                ),
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(build_session("products/my-app"))
```

### TypeScript

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

const BUILDER_PROMPT = `You are the Builder for this project.
// ... (same prompt as Python example above)
`;

const QA_PROMPT = `You are the QA Reviewer for this project.
// ... (same prompt as Python example above)
`;

async function buildSession(productPath: string) {
  for await (const message of query({
    prompt: `Run a build session for the product at ${productPath}.
1. Use the builder agent to implement the next item from mvp-specs/
2. After the builder finishes, use the qa-reviewer agent to verify the work
3. Report the combined results.`,
    options: {
      allowedTools: [
        "Read", "Edit", "Write", "Bash",
        "Glob", "Grep", "Agent",
      ],
      agents: {
        "builder": {
          description: "Builds product features from specs. Use for all code implementation tasks.",
          prompt: BUILDER_PROMPT,
          tools: ["Read", "Edit", "Write", "Bash", "Glob", "Grep"],
          model: "sonnet",
        },
        "qa-reviewer": {
          description: "Reviews code for quality and security. Use after builder completes work.",
          tools: ["Read", "Bash", "Glob", "Grep"],
          model: "sonnet",
        },
      },
    },
  })) {
    if ("result" in message) console.log(message.result);
  }
}

buildSession("products/my-app");
```

---

## Tool restriction patterns for PA·co roles

Each PA·co role maps to a specific tool restriction pattern in the SDK:

| PA·co role | SDK `tools` | Rationale |
|-----------|-------------|-----------|
| **Builder** | `["Read", "Edit", "Write", "Bash", "Glob", "Grep"]` | Full access — needs to build and deploy |
| **Auditor** | `["Read", "Glob", "Grep"]` | Read-only — must not modify what it audits |
| **QA** | `["Read", "Bash", "Glob", "Grep"]` | Can run tests but not edit source code |
| **Researcher** | `["Read", "Glob", "Grep", "WebSearch", "WebFetch"]` | Can search and read, not modify files |
| **Marketer** | `["Read", "Write", "Glob", "Grep"]` | Writes content files but no shell access |
| **Security** | `["Read", "Bash", "Glob", "Grep"]` | Scans for vulnerabilities, reports only |

These map directly to the `tools_allowed` / `tools_denied` patterns in [agent-schema.md](../core/agent-schema.md).

---

## Parallel agent execution

The SDK can run multiple subagents concurrently. Use this for PA·co's Refine phase, where all departments work in parallel:

```python
async def refine_phase(spec_path: str):
    """All departments refine a spec simultaneously."""
    async for message in query(
        prompt=f"""Refine the product spec at {spec_path}.

Run ALL of these agents in parallel:
1. engineering-reviewer — technical feasibility and architecture
2. security-reviewer — threat model and compliance requirements
3. market-reviewer — competitive landscape and positioning

Each agent should produce its enrichment as structured markdown.
Combine all outputs into a single refined spec.""",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "WebSearch", "Agent"],
            agents={
                "engineering-reviewer": AgentDefinition(
                    description="Reviews specs for technical feasibility.",
                    prompt="You are the Engineering reviewer...",
                    tools=["Read", "Glob", "Grep"],
                    model="sonnet",
                ),
                "security-reviewer": AgentDefinition(
                    description="Reviews specs for security and compliance.",
                    prompt="You are the Security reviewer...",
                    tools=["Read", "Glob", "Grep"],
                    model="sonnet",
                ),
                "market-reviewer": AgentDefinition(
                    description="Reviews specs for market fit and competition.",
                    prompt="You are the Market Intelligence reviewer...",
                    tools=["Read", "Glob", "Grep", "WebSearch"],
                    model="sonnet",
                ),
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)
```

---

## Context isolation in PA·co

Subagent context isolation maps naturally to PA·co's 4-layer Context Engineering:

| PA·co layer | What the subagent sees |
|-------------|----------------------|
| **Identity** | The `prompt` field (agent instructions) + project CLAUDE.md (auto-loaded) |
| **State** | Whatever file paths you pass in the Agent tool's prompt string |
| **Relevant** | Not automatic — include RAG results in the prompt if needed |
| **Archive** | Not available — subagents don't access pgvector directly |

To pass state context to a subagent, include file paths in the spawn prompt:

```python
# The orchestrator includes state context in the subagent prompt
prompt=f"""Review the product at products/my-app/.
Read these files for context:
- products/my-app/STATE.md (current progress)
- products/my-app/mvp-specs/SPEC_MVP_ENGINEERING.md (what to build)
- state/PIPELINE.md (pipeline status)
"""
```

---

## When to use file-based vs. SDK subagents

### Use file-based agents (`.claude/agents/`) when:

- Running agents via Claude Code CLI or Desktop
- Using Claude Code scheduled tasks
- You want zero-code agent management (edit markdown, not code)
- Agent definitions change frequently (non-technical team members edit them)

### Use SDK subagents when:

- Building a custom application that orchestrates PA·co agents
- Integrating PA·co into CI/CD pipelines
- You need programmatic control over agent spawning (dynamic configs, conditional agents)
- Running agents from a server or API endpoint
- You need parallel execution with result aggregation

### Use both together:

The SDK loads `.claude/agents/` files automatically. You can define base agents as files and override or extend them programmatically:

```python
# SDK agents override file-based agents with the same name
agents={
    # This overrides .claude/agents/builder.md for this session
    "builder": AgentDefinition(
        description="Builder with extra security constraints",
        prompt=BUILDER_PROMPT + "\n\nADDITIONAL: Run npm audit before every commit.",
        tools=["Read", "Edit", "Write", "Bash", "Glob", "Grep"],
    ),
    # .claude/agents/qa-reviewer.md still loads from filesystem
}
```

---

## Migrating from dispatch-only to subagents

If you're using PA·co's file-based dispatch today and want to add SDK subagents:

1. **Keep dispatch files.** Subagents don't replace dispatch — they're a spawn mechanism, not a coordination mechanism. Agents still coordinate through STATE.md and dispatch files.

2. **Start with the orchestrator.** Convert your orchestrator (PA·co) to an SDK application that spawns other agents as subagents. The orchestrator reads PIPELINE.md, decides which agents to run, and spawns them.

3. **Add tool restrictions.** Use the `tools` field to enforce least privilege. This is the biggest win — file-based agents declare restrictions but can't enforce them. SDK subagents enforce them at the API level.

4. **Keep agent prompts in markdown.** Load your `.claude/agents/*.md` files and pass their content as the `prompt` field. This keeps agent definitions editable without code changes:

```python
from pathlib import Path

def load_agent(name: str) -> AgentDefinition:
    """Load a PA·co agent file as an SDK AgentDefinition."""
    content = Path(f".claude/agents/{name}.md").read_text()
    # Parse YAML frontmatter for metadata
    # (use your preferred YAML parser)
    return AgentDefinition(
        description=f"PA·co {name} agent",
        prompt=content,
        tools=resolve_tools(parse_frontmatter(content)),
    )
```

---

## Limitations

- **Subagents cannot spawn subagents.** Don't include `Agent` in a subagent's `tools`. Nesting is one level deep.
- **No shared memory between subagents.** Each subagent has its own context. Coordinate through files (PA·co's dispatch pattern) or aggregate results in the parent.
- **Windows prompt length.** On Windows, keep subagent prompts under ~8000 characters due to command line limits. Use filesystem-based agents for long instructions.
- **No automatic RAG.** Subagents don't run pgvector queries. Pass relevant context in the spawn prompt or pre-cache it to a file the subagent can read.

---

## Related

- [Agent Schema](../core/agent-schema.md) — PA·co agent file format with tool whitelisting
- [A2A Protocol](a2a-protocol.md) — how agents coordinate work
- [Adding Agents](adding-agents.md) — create new file-based agents
- [Anthropic SDK docs](https://platform.claude.com/docs/en/agent-sdk/subagents) — official Subagents API reference
