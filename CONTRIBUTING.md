# Contributing to PA-co Framework

Thank you for your interest in contributing to PA-co. This guide explains how to participate, what we accept, and how to make the process smooth for everyone.

---

## What We Accept

**Yes -- we welcome these contributions:**

- **New agent templates** -- specialized agent roles (e.g., data-engineer.md, content-writer.md, compliance-officer.md)
- **New industry templates** -- complete multi-agent configurations for specific use cases (e.g., e-commerce, legal firm, content agency, dev team)
- **New department configurations** -- department dispatch structures for domains we haven't covered
- **Documentation improvements** -- typo fixes, clearer explanations, additional examples, translations
- **Bug reports** -- broken bootstrap flows, incorrect file references, template generation issues
- **Feature requests** -- ideas for new framework capabilities (file an issue first)

**No -- we do not accept these:**

- Penguin Alley-specific business logic, market intel, or internal processes
- Changes that break backward compatibility with existing templates without discussion
- Vendor-specific integrations that lock the framework to a paid service (the framework must remain zero-cost at its core)
- AI model-specific code that prevents the framework from working with future Claude versions

---

## How to Submit a Template

Templates are the most valuable contribution. Here is how to create one.

### Agent Template

1. Create a markdown file following the schema in `core/agent-schema.md`
2. Your agent must define:
   - A clear role and mission
   - An "I DO" section (what this agent is responsible for)
   - An "I DO NOT" section (what belongs to other agents)
   - Which dispatch files it reads and writes
   - Its expected run frequency
3. Place it in the appropriate template directory (e.g., `templates/your-template-name/.claude/agents/`)

### Industry Template

1. Create a new directory under `templates/` with a descriptive name (e.g., `templates/content-agency/`)
2. Include at minimum:
   - `CLAUDE.md` -- master rules file with `{{placeholders}}` for user-specific values
   - `.claude/agents/` -- all agent files for this configuration
   - `dispatch/` -- HALT.md, GENERAL.md, and department dispatches
   - `memory/` -- MEMORY.md index and lessons-learned.md starter
3. Use `{{PLACEHOLDER}}` syntax for anything that should be filled in during bootstrap (project name, CEO name, mission, etc.)
4. Include a brief README in the template directory explaining who this template is for and what agents it includes

---

## How to Report Issues

1. Open a GitHub Issue
2. Use a clear, descriptive title
3. Include:
   - What you expected to happen
   - What actually happened
   - Steps to reproduce (if applicable)
   - Your Claude Code version (CLI, Desktop, or VS Code extension)
   - Which template you were using

For security vulnerabilities, do NOT open a public issue. Email hello@penguinalley.com instead.

---

## Pull Request Guidelines

1. **Fork the repo** and create a branch from `main`
2. **One PR per contribution** -- do not bundle unrelated changes
3. **Describe your change** in the PR description: what it does, why it is needed, and how you tested it
4. **Test your changes** before submitting (see Testing below)
5. **Keep it focused** -- small, reviewable PRs are merged faster than large ones

### PR Title Format

Use a clear prefix:
- `template: add [name] industry template`
- `agent: add [name] agent template`
- `docs: fix typo in getting-started.md`
- `fix: correct dispatch reference in solo-founder template`
- `feat: add [feature] to bootstrap prompt`

### Review Process

- A maintainer will review your PR within 7 days
- We may request changes -- this is normal and not a rejection
- Once approved, a maintainer will merge

---

## Testing Your Changes

Before submitting a PR, verify your changes work:

1. **Start with a blank directory** -- create an empty folder with no existing PA-co files
2. **Run the bootstrap prompt** -- paste `paco-bootstrap.md` into Claude Code and go through the setup flow
3. **Select the template you modified** (or the closest match)
4. **Verify all files are created** -- check that every agent, dispatch, and memory file referenced in CLAUDE.md actually exists
5. **Run a standup** -- tell Claude Code "Run as /paco -- execute daily standup" and verify no errors
6. **Check cross-references** -- every agent should reference dispatch files that exist, every dispatch should reference agents that exist

If you are adding a new template:
- Run the full bootstrap with your template selected
- Verify every agent can run independently without errors
- Verify the dispatch system has no orphaned references

---

## Code of Conduct

This project follows a simple, professional standard.

**Expected behavior:**
- Be respectful and constructive in all interactions
- Welcome newcomers and help them get oriented
- Focus feedback on the contribution, not the contributor
- Assume good intent

**Unacceptable behavior:**
- Harassment, discrimination, or personal attacks of any kind
- Publishing others' private information without permission
- Trolling, insulting, or derogatory comments
- Any conduct that would be inappropriate in a professional setting

**Enforcement:**
- Violations will be addressed by maintainers privately first
- Repeated or severe violations result in temporary or permanent ban from the project
- Reports can be sent to conduct@penguinalley.com

---

## Questions?

- Open a GitHub Discussion for general questions
- Check the [FAQ](docs/faq.md) for common answers
- For framework-specific help, include your CLAUDE.md and the error output in your question

---

**PA-co Framework is built by [Penguin Alley](https://penguinalley.com).**
