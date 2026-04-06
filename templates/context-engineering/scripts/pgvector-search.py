"""
PA·co Context Engineering — Semantic Search Script
Searches the paco_knowledge table for entries relevant to a query.

Usage:
  python scripts/pgvector-search.py "your search query"
  python scripts/pgvector-search.py "deploy lessons" --type=lesson
  python scripts/pgvector-search.py "competitor pricing" --scope=my-product --limit=10

Returns: top N results ranked by semantic similarity with content + metadata.

Setup:
  1. Run schema.sql in your Supabase project
  2. Ingest some knowledge with pgvector-ingest.py
  3. Set SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY
"""
import os
import sys
import json
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://YOUR_PROJECT.supabase.co")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def load_env_file():
    """Load .env file if it exists."""
    global SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY
    env_path = os.path.join(REPO_ROOT, ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            val = val.strip().strip('"').strip("'")
            if key.strip() == "SUPABASE_URL":
                SUPABASE_URL = val
            elif key.strip() == "SUPABASE_SERVICE_KEY":
                SUPABASE_SERVICE_KEY = val
            elif key.strip() == "OPENAI_API_KEY":
                OPENAI_API_KEY = val


def get_embedding(text):
    """Generate embedding via OpenAI text-embedding-3-small."""
    payload = json.dumps({
        "model": "text-embedding-3-small",
        "input": text[:8000]
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/embeddings",
        data=payload,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode())
    return data["data"][0]["embedding"]


def search_knowledge(query_embedding, limit=5, filter_type=None, filter_scope=None):
    """Call the match_knowledge RPC function in Supabase."""
    params = {
        "query_embedding": query_embedding,
        "match_count": limit,
    }
    if filter_type:
        params["filter_type"] = filter_type
    if filter_scope:
        params["filter_scope"] = filter_scope

    payload = json.dumps(params).encode("utf-8")
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/rpc/match_knowledge",
        data=payload,
        headers={
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode())


def main():
    load_env_file()

    if not SUPABASE_SERVICE_KEY or not OPENAI_API_KEY:
        print("Error: Set SUPABASE_SERVICE_KEY and OPENAI_API_KEY", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python pgvector-search.py \"query\" [--type=X] [--scope=X] [--limit=N]")
        sys.exit(1)

    query = sys.argv[1]
    limit = 5
    filter_type = None
    filter_scope = None

    for arg in sys.argv[2:]:
        if arg.startswith("--type="):
            filter_type = arg.split("=", 1)[1]
        elif arg.startswith("--scope="):
            filter_scope = arg.split("=", 1)[1]
        elif arg.startswith("--limit="):
            limit = int(arg.split("=", 1)[1])

    embedding = get_embedding(query)
    results = search_knowledge(embedding, limit, filter_type, filter_scope)

    if not results:
        print("No results found.")
        return

    for i, r in enumerate(results, 1):
        sim = r.get("similarity", 0)
        meta = r.get("metadata", {})
        content = r.get("content", "")
        meta_type = meta.get("type", "?")
        scope = meta.get("scope", "?")
        source = meta.get("source", "?")
        print(f"--- Result {i} (similarity: {sim:.3f}) ---")
        print(f"Type: {meta_type} | Scope: {scope} | Source: {source}")
        print(content[:500])
        if len(content) > 500:
            print("... [truncated]")
        print()


if __name__ == "__main__":
    main()
