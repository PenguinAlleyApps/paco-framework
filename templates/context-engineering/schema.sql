-- PA·co Context Engineering — pgvector Schema
-- Run this in your Supabase SQL Editor or psql client.
-- Requires: Supabase project with pgvector extension enabled.

-- Step 1: Enable pgvector
create extension if not exists vector with schema extensions;

-- Step 2: Knowledge table — stores all organizational memory
create table if not exists paco_knowledge (
  id bigint primary key generated always as identity,
  content text not null,
  embedding extensions.vector(1536),  -- OpenAI text-embedding-3-small
  metadata jsonb not null default '{}',
  created_at timestamptz not null default now()
);

-- Step 3: Semantic search function
-- Returns the top N most similar entries to a query embedding.
create or replace function match_knowledge(
  query_embedding extensions.vector(1536),
  match_count int default 5,
  filter_type text default null,
  filter_scope text default null
)
returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    pk.id,
    pk.content,
    pk.metadata,
    1 - (pk.embedding <=> query_embedding) as similarity
  from paco_knowledge pk
  where
    (filter_type is null or pk.metadata->>'type' = filter_type)
    and (filter_scope is null or pk.metadata->>'scope' = filter_scope)
  order by pk.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- Step 4: Index for fast similarity search
create index if not exists idx_paco_knowledge_embedding
  on paco_knowledge
  using ivfflat (embedding extensions.vector_cosine_ops)
  with (lists = 100);

-- Step 5: Index on metadata for filtered queries
create index if not exists idx_paco_knowledge_metadata_type
  on paco_knowledge ((metadata->>'type'));

create index if not exists idx_paco_knowledge_metadata_scope
  on paco_knowledge ((metadata->>'scope'));

-- Metadata schema reference:
-- {
--   "type": "lesson|market_intel|competitive_intel|design_system|security|decision",
--   "scope": "universal|<product-name>",
--   "product": "<product-name>|null",
--   "department": "engineering|quality-security|intelligence|growth|governance|executive",
--   "tags": ["relevant", "tags"],
--   "source": "standup|session|research|audit",
--   "date": "YYYY-MM-DD"
-- }
