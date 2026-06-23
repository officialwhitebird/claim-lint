# Distribution Copy

## GitHub Repository Description

Experimental local-first CLI for scanning public text against explicit claim and internal-name rules.

## README Tagline Alternative

Check public-facing Markdown for configured overclaim and internal-name strings before release.

## X Post Drafts

1. I built `claim-lint`, a small experimental CLI that scans public-facing Markdown for configured overclaim phrases and internal project names before release. It is local-first, deterministic, and intentionally narrow.

2. `handoff-lint` checks the input side of an AI coding run. `claim-lint` checks the output copy before publication. Small tools, explicit rules, human judgment still in charge.

3. New garage artifact: `claim-lint` v0.1.0 candidate. JSON config, stable exit codes, text/JSON output, no LLM judgment, no hosted service. Built for checking explicit strings before public copy goes out.

## Longer Announcement Draft

I am preparing `claim-lint`, an experimental local-first CLI for checking public-facing Markdown before release.

The first version is intentionally simple: define prohibited claim strings and internal-name strings in `.claimlintrc.json`, then run `claim-lint scan README.md`. It reports matching lines, returns stable exit codes, and can emit JSON for automation.

This is not a semantic writing judge, not a credential scanner, and not a demand-validated product. It is a small garage tool for one release-prep boundary: catch explicit phrases that should not appear in public copy unless there is evidence for them.

It pairs naturally with `handoff-lint`: one checks the input to an AI coding run, the other checks the public output before publication.

## Short Video Script Outline

1. Show `.claimlintrc.json` with two rule groups.
2. Show an invalid README containing one overclaim phrase and one internal-name string.
3. Run `claim-lint scan`.
4. Point to line-numbered findings and exit code `1`.
5. Run the corrected README and show `No findings.` with exit code `0`.
6. Run `--json` to show automation-friendly output.
7. Close with the boundary: explicit string scanner, not semantic review.
