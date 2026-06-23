# Claims To Evidence

| Public claim | Allowed wording | Supporting evidence | Source | Risk if overstated | Safer fallback |
| --- | --- | --- | --- | --- | --- |
| Experimental | `experimental local-first CLI` | README explicitly marks the project as experimental. | `README.md` | Implies maturity beyond current release candidate. | `experimental release candidate` |
| Local-first | `runs from the local command line against local files` | CLI accepts local file paths and local config paths. | `claim_lint/cli.py` | Could imply full privacy guarantees beyond code scope. | `designed for local CLI use` |
| Offline | `does not define network calls or hosted service integration` | Runtime imports standard library and local modules only; no network libraries are used. | `claim_lint/*.py` | Could imply audited security/privacy guarantees. | `no network integration is implemented in v0.1.0` |
| Deterministic | `uses deterministic substring matching` | Scanner loops through configured strings and file lines. | `claim_lint/scanner.py` | Could imply complete or context-aware detection. | `deterministic for configured explicit strings` |
| JSON-only config | `uses .claimlintrc.json` | Config loader uses `json.load`; README documents JSON only. | `claim_lint/config.py`, `README.md` | Could imply formal JSON Schema validation beyond implementation. | `validates the required JSON object shape` |
| Python standard-library runtime | `has no runtime package dependencies` | `pyproject.toml` declares `dependencies = []`. | `pyproject.toml` | Could imply no dev dependency. | `runtime dependencies are empty; tests use pytest` |
| Scans explicit local rules | `scans configured prohibited_claims and internal_names` | Config schema and scanner support those lists. | `claim_lint/config.py`, `claim_lint/scanner.py` | Could imply built-in policy intelligence. | `scans explicit strings configured by the user` |
| Emits JSON | `supports --json output` | CLI builds a JSON object with `ok`, `summary`, and `findings`. | `claim_lint/cli.py` | Could imply a versioned formal API. | `emits a simple JSON report shape in v0.1.0` |
| No LLM judgment | `does not use LLM or semantic scoring` | No LLM dependency or network/API call is present. | `pyproject.toml`, `claim_lint/*.py` | Could imply better precision than string matching. | `performs no semantic judgment` |
| Not demand-validated | `not demand-validated` | Publication and response review have not occurred. | release projection status | Avoids unsupported adoption claims. | `not yet validated by external use` |
