# PA·co Memory System Schema

File-based persistent memory that survives across sessions. Every agent reads relevant memory files. Memory is institutional knowledge — not session notes.

## Directory Structure

```
memory/
  MEMORY.md                 — Master index (max 80 lines). Every agent reads this.
  lessons-learned.md        — Institutional memory. Every mistake → permanent rule. (max 50 active)
  decisions/                — Decision logs with reasoning. One file per decision.
    YYYY-MM-DD-[slug].md
  ideas/                    — Evaluated ideas/opportunities. One file per idea.
    [slug].md
  market-intel/             — Research findings, competitive analysis.
    YYYY-MM-DD-[slug].md
  reviews/                  — Retroactive product/process reviews.
    [slug].md
  security/
    scans/                  — Security scan reports.
    threat-models/          — Per-product threat models.
  finance/                  — Financial analyses, cost reviews.
  legal/                    — Legal reviews, compliance assessments.
  audits/                   — Quality audit reports.
```

## MEMORY.md (index file)

```markdown
# Memory Index

## Status: [project status summary]
## Date: [last updated]

## Active Reference:
- [file.md](file.md) — 1-line description

## Ideas:
- [idea-file.md](ideas/idea-file.md) — Status + 1-line description

## Market Intel:
- [intel-file.md](market-intel/intel-file.md) — 1-line description
```

**Rules:**
- Max 80 lines. If approaching limit, move stale entries to "Archived" section.
- Each entry is 1 line: `- [filename](path) — description`
- Update when adding new files.

## lessons-learned.md

```markdown
# Lessons Learned

**Every agent MUST read this before build, deploy, or audit sessions.**
**Any agent CAN add a lesson during their session.**

## [Category]
- **[Rule in bold.]** [Explanation of what happened, why, and what to do differently. Include source.]
```

**Rules:**
- Max 50 active lessons. When approaching limit, archive lessons already codified as permanent rules elsewhere.
- Every lesson has: the rule, the context, and the source (what incident caused it).
- A lesson graduates from here when the system CAN'T make that mistake anymore because it's enforced in an agent file, quality gate, or executive order.

## What goes in memory vs. what doesn't:

**YES — save to memory:**
- Decisions with reasoning (why we chose X over Y)
- Market intelligence that informs strategy
- Mistakes and their root causes
- Competitive analysis findings
- Financial/legal reviews

**NO — don't save to memory:**
- Session-specific work (that's in dispatch activity logs)
- Code or technical implementation details (that's in the codebase)
- Ephemeral status (that's in dispatch state sections)
- Anything derivable from git history
