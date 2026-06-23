# Contributing

claim-lint is a small experimental CLI. Contributions should keep the v0.1.0 boundary narrow and reproducible.

## Development Setup

```bash
python -m pip install -e .[dev]
python -m pytest -q
```

## Contribution Guidelines

- Keep runtime dependencies to the Python standard library unless a future release explicitly changes that boundary.
- Prefer deterministic behavior over subjective scoring.
- Do not add LLM calls, hosted services, background watchers, credential scanning, or autofix behavior to v0.1.0.
- Avoid public claims about adoption, demand validation, productivity gains, time savings, production readiness, enterprise readiness, or security-grade behavior.
- Add or update tests for behavior changes.

## Public Copy Guardrails

Public documentation should describe what claim-lint does with evidence from code and tests. If a claim cannot be traced to implementation or verification output, use a safer wording.
