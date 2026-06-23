# claim-lint Portfolio Case Study Draft

## Problem

AI-assisted release preparation can produce public-facing text that sounds more certain than the available evidence. It can also accidentally include project-specific internal names that should not appear in public copy.

## Design Principle

Keep the tool narrow, local, and explicit. claim-lint does not judge writing quality. It checks configured strings in local text files and reports deterministic findings before publication.

## What Was Built

claim-lint is an experimental Python CLI that scans Markdown or plain text files for two configured rule groups:

- `prohibited_claims`
- `internal_names`

It supports text output, JSON output, stable exit codes, and a JSON-only configuration file.

## Relationship To handoff-lint

handoff-lint checks work instructions before an AI coding run begins. claim-lint checks public-facing text after a run produces release or portfolio copy. Together, they form a small input/output guardrail pair for an AI-assisted development workflow.

## Demo Flow

1. Install the package locally.
2. Create `.claimlintrc.json`.
3. Run claim-lint against an intentionally invalid README.
4. Inspect the findings.
5. Run claim-lint against a corrected README.
6. Run the invalid example with `--json`.

## Verification Evidence

The v0.1.0 release candidate includes a pytest suite with 15 tests, a GitHub Actions CI workflow, demo fixtures, and a claims-to-evidence mapping.

## Boundaries And Non-Goals

claim-lint does not perform LLM judgment, semantic scoring, autofix, credential scanning, hosted service integration, or background monitoring. It is not demand-validated and should not be described as production-ready.

## Garage / Factory Fit

claim-lint fits the officialwhitebird garage direction: turn a small, observed AI workflow friction into a bounded public tool with explicit evidence and strict claim guardrails.
