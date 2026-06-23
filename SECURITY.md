# Security Policy

claim-lint is an experimental local-first CLI for scanning text against explicit local rules.

## Supported Versions

No public release has been published yet. Until v0.1.0 is published, security reports should refer to the current local release candidate.

## Reporting a Vulnerability

Please open a GitHub issue after the repository is public, or contact the maintainer through the officialwhitebird project channel used for the release.

Do not include secrets, private credentials, or confidential documents in a public report. Provide a minimal reproduction using synthetic text whenever possible.

## Security Boundary

claim-lint does not attempt to detect API keys, tokens, passwords, or other credentials. Use a dedicated secret scanner for that purpose.

claim-lint is not a security-grade scanner and should not be treated as a substitute for manual review or specialized security tooling.
