# Context Engineering Template — pgvector Setup

Add semantic memory to your PA·co system. Agents store lessons, decisions, and intel in a vector database and retrieve relevant context each session.

## What this gives you

Without this template, PA·co uses file-based memory (`memory/` directory). That works for small teams with <100 entries. This template upgrades you to **Layer 3: Relevant Context** — semantic search over all organizational knowledge.

| Layer | Before (files) | After (pgvector) |
|-------|----------------|-------------------|
| 3 — Relevant | Manual reads of `memory/*.md` | Auto-retrieved by semantic similarity |
| 4 — Archive | Files accumulate, context bloats | Grows forever, only relevant entries surfaced |

## Prerequisites

- **Supabase project** (free tier works) — [supabase.com](https://supabase.com)
- **OpenAI API key** — for `text-embedding-3-small` embeddings (~$0.02/1M tokens)
- **Python 3.8+** — no external dependencies (uses `urllib` only)

## Setup (5 minutes)

### 1. Create the database schema

Open your Supabase SQL Editor and run `schema.sql`:

```sql
-- Enables pgvector, creates paco_knowledge table,
-- creates match_knowledge() search function,
-- creates indexes for fast similarity search.
```

This creates one table (`paco_knowledge`) with columns: `content`, `embedding`, `metadata`, `created_at`.

### 2. Set environment variables

Create a `.env` file in your project root:

```bash
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_SERVICE_KEY=eyJ...your-service-role-key
OPENAI_API_KEY=sk-...your-openai-key
```

Find your service key in Supabase → Settings → API → `service_role` key.

### 3. Create the directory structure

```bash
mkdir -p output/lessons-pending output/decisions-pending output/ingested
cp templates/context-engineering/scripts/* scripts/
```

### 4. Test ingestion

Create a test file in `output/lessons-pending/2026-01-01-test.md`:

```markdown
---
type: lesson
scope: universal
department: engineering
tags: [test, setup]
source: session
---
WHEN: Setting up pgvector for the first time
THEN: Run schema.sql before attempting ingestion
NEVER: Use the anon key — always use service_role for server-side operations
BECAUSE: Anon key has RLS restrictions that block inserts
```

Run the ingestion:

```bash
python scripts/pgvector-ingest.py
# Output: Done: 1/1 ingested to pgvector
```

### 5. Test search

```bash
python scripts/pgvector-search.py "pgvector setup"
# Output: Result 1 (similarity: 0.85) — your test entry
```

## How agents use it

Add this to your agent session scripts or CLAUDE.md:

```markdown
## Session Start — Context Assembly
1. Read dispatch files (Layer 2: State)
2. Search pgvector for relevant context:
   python scripts/pgvector-search.py "{{task_description}}" --limit=5
3. Use returned knowledge to inform your work
```

### Automatic RAG pre-caching

For agents that can't run Python (e.g., browser-based sessions), pre-cache results:

```bash
# Run hourly in a cron or build session
python scripts/pgvector-search.py "distribution channels platforms" --limit=5 > state/rag-cache/distribution-context.md
```

Agents read the cached file instead of running the search themselves.

## Knowledge entry format

The recommended format for lessons (the most common entry type):

```markdown
---
type: lesson
scope: universal
product: my-product
department: engineering
tags: [deploy, vercel, dns]
source: session
---
WHEN: Deploying to Vercel with a custom domain
THEN: Verify DNS propagation before running health checks
NEVER: Assume DNS changes are instant — wait 5 minutes minimum
BECAUSE: 2026-03-15 deploy appeared broken due to DNS cache (TTL was 300s)
VERIFY: curl -I https://yourdomain.com returns 200
```

### Metadata types

| Type | When to use |
|------|-------------|
| `lesson` | Something went wrong (or right) and you want to remember it |
| `decision` | A significant choice was made with reasoning |
| `market_intel` | Research findings about markets, trends, or opportunities |
| `competitive_intel` | Competitor analysis, pricing, features |
| `security` | Security findings, vulnerabilities, mitigations |
| `design_system` | Design patterns, component decisions, UX rules |

### Filter examples

```bash
# Only lessons
python scripts/pgvector-search.py "deploy" --type=lesson

# Only for a specific product
python scripts/pgvector-search.py "auth bug" --scope=my-product

# More results
python scripts/pgvector-search.py "pricing strategy" --limit=10
```

## Scaling notes

- **Free tier Supabase** handles ~50K entries comfortably
- **IVFFlat index** (in schema.sql) is optimized for <100K rows. For larger datasets, consider HNSW indexing
- **Embedding cost**: ~$0.02 per 1M tokens. A typical lesson is ~200 tokens → 5,000 lessons for $0.02
- **Search latency**: <100ms for 50K entries on Supabase free tier

## File structure

```
templates/context-engineering/
  README.md          ← This file
  schema.sql         ← Database schema (run in Supabase SQL Editor)
  scripts/
    pgvector-ingest.py   ← Ingestion script (copy to your scripts/)
    pgvector-search.py   ← Search script (copy to your scripts/)
```

## Without pgvector

If you don't want to set up a vector database, PA·co still works with file-based memory. See `core/context-engineering.md` section "Without a Vector DB" for the fallback approach. You can migrate to pgvector later — the entry format is the same.

---

Built by PA·co — A Penguin Alley System | [penguinalley.com](https://penguinalley.com)
