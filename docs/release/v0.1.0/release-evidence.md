# claim-lint v0.1.0 Release Evidence

Status: local release candidate; not yet published.

## Package

- Package name: `claim-lint`
- Version: `0.1.0`
- Python version floor: `>=3.10`
- Runtime dependencies: none declared
- Development dependency: `pytest>=7.0.0`
- License: MIT

## Install And Test

Commands used for this projection:

```bash
python -m pip install -e .[dev]
python -m pytest -q
```

Observed test result on 2026-06-24 JST:

```text
...............                                                          [100%]
15 passed in 0.19s
```

## Representative CLI Checks

Fixture config:

```text
docs/release/v0.1.0/fixtures/.claimlintrc.json
```

Invalid input:

```bash
claim-lint scan docs/release/v0.1.0/fixtures/invalid-readme.md --config docs/release/v0.1.0/fixtures/.claimlintrc.json
```

Observed output:

```text
ERROR claim.prohibited [line 3]: matched 'drastically' (rule: prohibited_claims) -> Remove unevidenced performance claim.
ERROR internal-name.detected [line 4]: matched 'PrivateCodename' (rule: internal_names) -> Remove internal project name leak.
EXIT_CODE=1
```

Valid input:

```bash
claim-lint scan docs/release/v0.1.0/fixtures/valid-readme.md --config docs/release/v0.1.0/fixtures/.claimlintrc.json
```

Observed output:

```text
No findings.
EXIT_CODE=0
```

JSON output:

```bash
claim-lint scan docs/release/v0.1.0/fixtures/invalid-readme.md --config docs/release/v0.1.0/fixtures/.claimlintrc.json --json
```

Observed output:

```text
{
  "ok": false,
  "summary": {
    "total_errors": 2
  },
  "findings": [
    {
      "severity": "ERROR",
      "code": "claim.prohibited",
      "line": 3,
      "matched_text": "drastically",
      "rule_source": "prohibited_claims",
      "repair_guidance": "Remove unevidenced performance claim."
    },
    {
      "severity": "ERROR",
      "code": "internal-name.detected",
      "line": 4,
      "matched_text": "PrivateCodename",
      "rule_source": "internal_names",
      "repair_guidance": "Remove internal project name leak."
    }
  ]
}
EXIT_CODE=1
```

## Offline And Privacy Boundary

claim-lint scans local files using explicit local JSON rules. The runtime code imports only Python standard library modules and local package modules. It does not define network calls or hosted service integration.

## CI Presence

`.github/workflows/ci.yml` exists and runs tests on:

- `ubuntu-latest`
- `windows-latest`
- Python `3.10`, `3.11`, `3.12`

## Known Limitations

- Matching is case-insensitive exact substring matching.
- It does not perform semantic or contextual judgment.
- It does not scan credentials or secrets.
- It does not autofix text.
- It does not ignore Markdown code blocks or quoted examples. If configured terms appear in documentation examples or guardrail lists, they are still reported.
- It is not demand-validated and has not been published yet.
