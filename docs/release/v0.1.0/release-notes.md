# claim-lint v0.1.0

Initial experimental release of claim-lint.

claim-lint is a local-first CLI for scanning public-facing Markdown or plain text against explicit local rules for:

- configured overclaim strings
- configured internal-name strings

## Included

- `claim-lint scan <file_path>`
- `--config <config_path>`
- `--json`
- JSON-only `.claimlintrc.json`
- stable exit codes:
  - `0`: no findings
  - `1`: configured claim or internal-name finding
  - `2`: operational or config error
- pytest test suite
- GitHub Actions CI
- release evidence and claims-to-evidence docs

## Boundaries

This release does not perform semantic judgment, LLM review, credential scanning, autofix, hosted service integration, or background monitoring.

It is not demand-validated and should not be treated as production-ready.

## Verification

Local release projection verification:

```text
python -m pytest -q
15 passed in 0.19s
```

Representative CLI checks are documented in `docs/release/v0.1.0/release-evidence.md`.
