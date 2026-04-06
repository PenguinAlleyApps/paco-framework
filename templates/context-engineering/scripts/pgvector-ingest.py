"""
PA·co Context Engineering — Knowledge Ingestion Script
Reads markdown files from pending directories, generates embeddings,
and inserts them into the paco_knowledge table via Supabase.

Usage: python scripts/pgvector-ingest.py

Setup:
  1. Run schema.sql in your Supabase project
  2. Set environment variables (see .env.example)
  3. Place markdown files in output/lessons-pending/ or output/decisions-pending/
  4. Run this script — files are moved to output/ingested/ after insert

Markdown file format:
  ---
  type: lesson
  scope: universal
  product: my-product
  department: engineering
  tags: [deploy, vercel]
  source: session
  ---
  Your content here. Can be multi-line. The frontmatter becomes metadata,
  the body becomes the searchable content.
"""
import os
import sys
import json
import glob
import shutil
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

# --- Configuration (edit these or set env vars) ---
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://YOUR_PROJECT.supabase.co")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

INGESTED_DIR = os.path.join(REPO_ROOT, "output", "ingested")
PENDING_DIRS = [
    os.path.join(REPO_ROOT, "output", "lessons-pending"),
    os.path.join(REPO_ROOT, "output", "decisions-pending"),
]


def load_env_file():
    """Load .env file if it exists (simple key=value parser)."""
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


def parse_frontmatter(text):
    """Extract YAML-like frontmatter and body from markdown."""
    metadata = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].strip()
            for line in parts[1].strip().split("\n"):
                if ":" not in line:
                    continue
                key, _, val = line.partition(":")
                val = val.strip()
                if val.startswith("[") and val.endswith("]"):
                    val = [v.strip().strip('"').strip("'")
                           for v in val[1:-1].split(",") if v.strip()]
                metadata[key.strip()] = val
    return metadata, body


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


def insert_knowledge(content, embedding, metadata):
    """Insert a knowledge entry into Supabase paco_knowledge table."""
    payload = json.dumps({
        "content": content,
        "embedding": embedding,
        "metadata": metadata,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/paco_knowledge",
        data=payload,
        headers={
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
        method="POST",
    )
    urllib.request.urlopen(req)


def main():
    load_env_file()

    if not SUPABASE_SERVICE_KEY or not OPENAI_API_KEY:
        print("Error: Set SUPABASE_SERVICE_KEY and OPENAI_API_KEY", file=sys.stderr)
        sys.exit(1)

    os.makedirs(INGESTED_DIR, exist_ok=True)
    for d in PENDING_DIRS:
        os.makedirs(d, exist_ok=True)

    pending = []
    for d in PENDING_DIRS:
        pending.extend(glob.glob(os.path.join(d, "*.md")))

    ingested = 0
    for filepath in pending:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        metadata, body = parse_frontmatter(text)
        if not body.strip():
            continue

        metadata.setdefault("date", os.path.basename(filepath)[:10])
        metadata.setdefault("type", "lesson")
        metadata.setdefault("scope", "universal")

        embedding = get_embedding(body)
        insert_knowledge(body, embedding, metadata)

        dest = os.path.join(INGESTED_DIR, os.path.basename(filepath))
        shutil.move(filepath, dest)
        ingested += 1

    print(f"Done: {ingested}/{len(pending)} ingested to pgvector")


if __name__ == "__main__":
    main()
