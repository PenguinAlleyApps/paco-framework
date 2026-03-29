# Lessons Learned

**Every agent MUST read this before build, deploy, or audit sessions.**
**Any agent CAN add a lesson during their session.**

---

## Getting Started
- **Read dispatch files BEFORE doing anything.** If you skip dispatch, you risk contradicting what another agent already decided.
- **Save findings to memory/ immediately.** Sessions are ephemeral — if it's not in a file, it didn't happen.
- **Health checks verify infrastructure, not user experience.** Tables existing does NOT mean users can complete the core flow.
- **Every table with RLS needs policies for ALL operations the code performs.** If code does an upsert, the table needs BOTH INSERT and UPDATE policies.
- **Run database migrations on production, not just create the files.** Creating a migration file does NOT apply it.

---

*To add a lesson: describe what happened, why, and what to do differently. Include the source.*
