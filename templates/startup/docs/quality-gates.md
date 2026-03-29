# Quality Gates

Universal checks that apply to all significant outputs before they reach the CEO.

## Pre-Deploy Checklist
- [ ] Health endpoint returns 200
- [ ] Core user flow works end-to-end (not just health check)
- [ ] Database migrations applied to production (not just created)
- [ ] No credentials in committed code
- [ ] Security headers present (CSP, HSTS, X-Frame-Options)
- [ ] Interactive elements have loading states (no silent buttons)

## Pre-Launch Checklist
- [ ] Every claim on landing page is backed by functional code
- [ ] Pricing tiers match code-level access gates
- [ ] Privacy policy exists and is accurate
- [ ] Terms of service exist
- [ ] AI disclaimer visible if product uses AI
- [ ] "Powered by [Brand]" attribution present
- [ ] Cookie consent if using analytics

## Content Checklist
- [ ] No false claims about product capabilities
- [ ] No competitor bashing
- [ ] Data/claims backed by sources
- [ ] Visual included (no text-only posts)
- [ ] Content mix maintained (70% educational, 20% product, 10% brand)

## Research Checklist
- [ ] Every claim has a source URL
- [ ] Competitor analysis includes: features, pricing, funding, growth
- [ ] Recommendations include risks and alternatives
- [ ] Findings saved to memory/ (not just in session)

## Audit Checklist
- [ ] Promises vs Reality: does the product do what we claim?
- [ ] EO compliance: are all executive orders being followed?
- [ ] Lessons learned: are past mistakes being avoided?
- [ ] Dispatch hygiene: are files under size limits?
