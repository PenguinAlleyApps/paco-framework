# MCP Transports

How PA·co agents connect to external tools and services via the Model Context Protocol.

---

## What is MCP

MCP (Model Context Protocol) is Anthropic's open standard for connecting AI agents to external tools and data sources. Claude Code supports MCP natively -- agents can use MCP servers to interact with databases, APIs, cloud platforms, and local services without writing custom integration code.

In PA·co, MCP servers extend what agents can do beyond the built-in Claude Code tools (Read, Write, Bash, Glob, Grep). A Builder agent might use an MCP server for Supabase to manage databases. A Researcher agent might use one for web search. A DevOps agent might use one for Cloudflare Workers.

---

## The three transports

MCP supports three transport mechanisms for connecting Claude Code to MCP servers. Each transport defines how the client (Claude Code) communicates with the server process.

| Transport | Protocol | Best for | Latency | Setup complexity |
|-----------|----------|----------|---------|-----------------|
| **Stdio** | stdin/stdout | Local CLI tools, bundled servers | Lowest | Simplest |
| **SSE** | HTTP + Server-Sent Events | Remote servers, shared infrastructure | Medium | Moderate |
| **Streamable HTTP** | HTTP POST/GET with streaming | Production APIs, scalable services | Medium | Moderate |

### Stdio (local process)

The server runs as a child process on the same machine. Claude Code communicates via stdin/stdout pipes. This is the default and most common transport.

**When to use:** Local tools, development, single-machine setups, most PA·co deployments.

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}"
      }
    }
  }
}
```

**How it works:**
1. Claude Code spawns the process (`npx @supabase/mcp-server`)
2. Sends JSON-RPC messages to the process's stdin
3. Reads JSON-RPC responses from the process's stdout
4. The process stays alive for the duration of the session

### SSE (Server-Sent Events)

The server runs as an HTTP service. Claude Code connects via an SSE endpoint for server-to-client streaming and sends requests via HTTP POST.

**When to use:** Remote servers, shared team infrastructure, servers that need to persist across sessions.

```json
{
  "mcpServers": {
    "my-remote-server": {
      "url": "https://mcp.example.com/sse"
    }
  }
}
```

**How it works:**
1. Claude Code opens an SSE connection to the server URL
2. Sends tool calls as HTTP POST requests
3. Receives streaming responses via the SSE channel
4. Connection persists for the session duration

### Streamable HTTP

The newest transport. The server exposes a single HTTP endpoint. Claude Code sends requests and receives responses -- optionally streamed -- over standard HTTP.

**When to use:** Production deployments, serverless environments (Cloudflare Workers, AWS Lambda), when SSE long-lived connections are impractical.

```json
{
  "mcpServers": {
    "my-api-server": {
      "url": "https://mcp.example.com/mcp"
    }
  }
}
```

**How it works:**
1. Claude Code sends JSON-RPC requests via HTTP POST
2. Server responds with JSON-RPC responses (optionally streamed)
3. No persistent connection required -- each request is independent
4. Ideal for stateless or serverless server implementations

---

## Configuring MCP servers

MCP servers are configured in `.claude/settings.json` (project-level) or `~/.claude/settings.json` (global). Project-level settings are recommended for PA·co so all agents in the project share the same tool access.

### Project-level configuration

```json
// .claude/settings.json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}"
      }
    },
    "stripe": {
      "command": "npx",
      "args": ["-y", "@stripe/mcp"],
      "env": {
        "STRIPE_SECRET_KEY": "${STRIPE_SECRET_KEY}"
      }
    },
    "cloudflare": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/cloudflare-mcp-server"]
    }
  }
}
```

### Environment variable resolution

Use `${VAR_NAME}` syntax to reference environment variables. Claude Code resolves these at runtime from the shell environment or `.env` files. Never hardcode secrets in settings files.

### Verifying MCP server availability

After configuring, verify servers are loaded:

```bash
# In Claude Code, the /mcp command shows connected servers
/mcp
```

Each connected server exposes tools that become available to agents during their sessions.

---

## MCP in PA·co's agent model

### Per-agent tool control

PA·co's `tools_allowed` and `tools_denied` fields in agent definitions apply to MCP tools the same way they apply to built-in tools. MCP tools are namespaced as `mcp__[server]__[tool]`.

```yaml
---
name: "Database Admin"
tools_allowed: ["Read", "Glob", "Grep", "mcp__supabase__query", "mcp__supabase__list_tables"]
tools_denied: []
---
```

This agent can only read files and use two specific Supabase MCP tools. It cannot write files, run shell commands, or use any other MCP server.

### Recommended MCP restrictions by role

| PA·co role | MCP access | Rationale |
|-----------|------------|-----------|
| **Builder** | All configured MCP servers | Needs full access to build and deploy |
| **Auditor** | Read-only MCP tools only | Must not modify what it audits |
| **QA** | Test/query tools, no mutations | Can verify state but not change it |
| **Researcher** | Web search MCPs, no infrastructure | Research scope only |
| **DevOps** | Infrastructure MCPs (Cloudflare, Vercel) | Deployment and monitoring |
| **Marketer** | Content MCPs, no infrastructure | Content platforms, not databases |

### MCP tools in Subagents API

When spawning agents via the Claude Agent SDK, MCP tools are included in the `tools` array with their namespaced names:

```python
AgentDefinition(
    description="Database-aware builder",
    prompt=BUILDER_PROMPT,
    tools=[
        "Read", "Edit", "Write", "Bash",
        "mcp__supabase__query",
        "mcp__supabase__apply_migration",
    ],
    model="sonnet",
)
```

---

## Common MCP servers for multi-agent systems

These servers are particularly useful in PA·co-style multi-agent setups:

| Server | Transport | Use case |
|--------|-----------|----------|
| `@supabase/mcp-server` | Stdio | Database management, migrations, auth |
| `@stripe/mcp` | Stdio | Payment management, subscriptions |
| `@anthropic-ai/cloudflare-mcp-server` | Stdio | Workers, KV, R2, D1 deployment |
| `@anthropic-ai/github-mcp-server` | Stdio | Repository management, PRs, issues |
| `@anthropic-ai/linear-mcp-server` | Stdio | Issue tracking, project management |
| `@anthropic-ai/slack-mcp-server` | Stdio | Team notifications, channel management |

### Installing MCP servers

Most MCP servers are distributed as npm packages. Claude Code auto-installs them via `npx` on first use when configured with the `command: "npx"` pattern. No manual installation required.

For servers that need persistent state or background processes, install globally:

```bash
npm install -g @supabase/mcp-server
```

---

## Security considerations

MCP servers extend the attack surface of your agent system. Apply PA·co's security principles:

### Least privilege

Only configure MCP servers that agents actually need. Each server is a potential vector for data exposure or unintended mutations. If only the Builder needs Supabase access, don't configure it at the global level where all agents inherit it.

### Secret management

- Store MCP credentials in `.env` files, never in `.claude/settings.json`
- Use `${VAR_NAME}` references for all secrets
- Rotate credentials on a regular cadence
- Different products can use different `.env.local` files with product-specific credentials

### MCP server vetting

Before adding an MCP server to your PA·co system:

1. Verify the server source (official Anthropic, verified publisher, or audited open source)
2. Check the tool list -- does it expose more capabilities than you need?
3. Review the server's permission model -- can it be scoped to read-only?
4. Test in isolation before adding to the shared project configuration
5. Monitor for unexpected behavior during initial agent sessions

### Network exposure

- **Stdio servers** run locally with no network exposure. Preferred for security.
- **SSE/HTTP servers** expose network endpoints. Use HTTPS only. Authenticate all connections.
- Remote servers should run behind authentication (API keys, OAuth, mTLS).

---

## Choosing the right transport

```
Is the MCP server a local CLI tool or npm package?
  YES -> Use Stdio (simplest, most secure, no network exposure)
  NO  -> Is the server already running as an HTTP service?
    YES -> Does it support SSE?
      YES -> Use SSE (established, well-supported)
      NO  -> Use Streamable HTTP
    NO  -> Can you run it locally?
      YES -> Use Stdio
      NO  -> Deploy as HTTP service, use SSE or Streamable HTTP
```

For most PA·co deployments running on a single machine (the typical Claude Code setup), **Stdio is the right choice.** Use SSE or Streamable HTTP only when the MCP server must run on a different machine or as a shared service.

---

## Related

- [Architecture](architecture.md) -- system design and MCP integration points
- [Agent Schema](../core/agent-schema.md) -- tool whitelisting with `tools_allowed` / `tools_denied`
- [Subagents API](subagents.md) -- programmatic agent spawning with MCP tool restrictions
- [Adding Agents](adding-agents.md) -- create agents with specific MCP access
- [MCP specification](https://modelcontextprotocol.io) -- official protocol documentation
