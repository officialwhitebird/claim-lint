# Demo Script

Run from the repository root after installing the package locally.

## 1. Install

```bash
python -m pip install -e .[dev]
```

## 2. Inspect Config

```bash
type docs\release\v0.1.0\fixtures\.claimlintrc.json
```

On macOS/Linux:

```bash
cat docs/release/v0.1.0/fixtures/.claimlintrc.json
```

## 3. Run Invalid README

```bash
claim-lint scan docs/release/v0.1.0/fixtures/invalid-readme.md --config docs/release/v0.1.0/fixtures/.claimlintrc.json
```

Expected result: two findings and exit code `1`.

## 4. Run Corrected README

```bash
claim-lint scan docs/release/v0.1.0/fixtures/valid-readme.md --config docs/release/v0.1.0/fixtures/.claimlintrc.json
```

Expected result: `No findings.` and exit code `0`.

## 5. Run JSON Output

```bash
claim-lint scan docs/release/v0.1.0/fixtures/invalid-readme.md --config docs/release/v0.1.0/fixtures/.claimlintrc.json --json
```

Expected result: JSON report with `ok: false`, `total_errors: 2`, and two findings.
