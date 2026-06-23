# Publish Prep Checklist

Publication status: not published. Owner approval required before any external action.

## Repository

- Repository name: `claim-lint`
- Owner: `officialwhitebird`
- Visibility: public, only after owner approval
- Description: `Experimental local-first CLI for scanning public text against explicit claim and internal-name rules.`

## Topics

- `cli`
- `markdown`
- `lint`
- `local-first`
- `ai-coding`
- `release-tools`

## Release

- Tag name: `v0.1.0`
- Release title: `claim-lint v0.1.0`
- Release status: owner-gated

## Required Pre-Publish Checks

- `python -m pip install -e .[dev]`
- `python -m pytest -q`
- Invalid fixture scan exits `1`.
- Valid fixture scan exits `0`.
- Invalid fixture JSON scan exits `1`.
- `.gitignore`, `LICENSE`, `SECURITY.md`, and `CONTRIBUTING.md` exist.
- Generated artifacts are absent or ignored.
- Claims-to-evidence mapping is reviewed.
- README is scanned for prohibited internal/private terms before publication.
- If scanning docs that intentionally show invalid examples, review those findings as documented examples rather than unsupported public claims.

## Claim Guardrails

Do not claim:

- demand validation
- adoption
- productivity gain
- time savings
- reduced overhead
- production readiness
- enterprise readiness
- security-grade behavior
- semantic judgment

## Owner Approvals Required

- Create GitHub repository.
- Initialize git, commit, and push.
- Create tag and GitHub release.
- Post any external announcement.
- Pin or link the repository from profile/portfolio surfaces.
