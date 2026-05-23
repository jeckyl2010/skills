---
name: dependency-analysis
version: 1.0.0
description: Audit project dependencies for outdated versions, known CVEs, licensing risk, orphaned packages, and upgrade paths across any package manifest format.
tags: [dependencies, security, audit, modernization, npm, python, java, dotnet]
tool_agnostic: true
---

# Dependency Analysis

Audit project dependencies systematically — outdated versions, security vulnerabilities, licensing risk, orphaned packages, and viable upgrade paths.

## Use When

- Starting a modernization or technical assessment engagement
- Preparing a risk report on a codebase's external dependencies
- Before a major version upgrade to understand the blast radius
- When CVE exposure is a concern and no recent audit exists

## Do Not Use When

- The codebase has no external dependencies
- A recent (< 30 days) automated scan report already exists and covers the same scope

## Scope

Covers all major manifest formats:
- Node.js: `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- Python: `requirements.txt`, `pyproject.toml`, `Pipfile`, `poetry.lock`
- Java/Kotlin: `pom.xml`, `build.gradle`
- .NET: `*.csproj`, `packages.config`, `NuGet.lock`
- Go: `go.mod`, `go.sum`
- Rust: `Cargo.toml`, `Cargo.lock`
- Docker: `Dockerfile` base images

## Procedure

1. **Inventory all manifests.** Locate every dependency file in the repository. Note which are production dependencies vs. dev/test.

2. **Identify outdated packages.**
   - Flag packages more than 2 major versions behind current
   - Flag packages with no release activity in the past 18 months
   - Note semantic versioning discipline: pinned vs. range vs. floating

3. **Check for known CVEs.**
   Use available tooling or known vulnerability databases (NVD, OSV, GitHub Advisory Database, Snyk). Flag severity: Critical / High / Medium / Low.

4. **Assess licensing risk.**
   - Identify any GPL/AGPL/EUPL licenses in production dependencies — these may impose copyleft obligations
   - Flag unknown or non-standard licenses
   - Note any license incompatibilities with the project's own license

5. **Identify orphaned or abandoned packages.**
   - No recent commits, no response to issues, no maintainer activity
   - These are a supply-chain risk even without a current CVE

6. **Assess upgrade complexity.**
   For each critical/high finding, estimate upgrade effort:
   - Drop-in: minor/patch version, no API changes
   - Moderate: major version with migration guide
   - Complex: breaking changes, peer dependency conflicts, or no direct upgrade path

7. **Identify transitive risk.**
   Note where a vulnerable dependency is pulled in transitively (not a direct dependency). These are harder to remediate but still carry risk.

## Output Shape

### Summary
Total dependency count, count by status (up to date / outdated / critical / abandoned), and top-line risk assessment.

### Critical and High Findings
One entry per finding:
- Package name and current version
- Latest stable version
- CVE ID(s) if applicable, with severity
- Upgrade path or recommended action

### Licensing Findings
Packages with license concerns, the specific license, and the implication.

### Maintenance Risk
Abandoned or unmaintained packages and their role in the dependency graph.

### Recommendations
Prioritized action list:
1. Immediate: critical CVEs and actively exploited vulnerabilities
2. Short-term: high CVEs and abandoned packages in critical paths
3. Planned: version hygiene and licensing cleanup

## Executing the update (Bun workspaces)
After auditing, the update sequence is:
1. `cd <workspace> && bun update` — bumps all packages to latest matching semver
2. `bun run typecheck` — verify no type regressions before running tests
3. Run the full test suite only after typecheck is clean
4. Pay extra attention to major-version library bumps (e.g. Zod 3→4, React 18→19) — check for breaking API changes in `safeParse`, schema declarations, type inference

## Common Mistakes To Avoid

- Treating dev dependencies as low-risk without checking build-chain exposure
- Ignoring transitive dependencies — many CVEs are introduced transitively
- Recommending "upgrade everything" without assessing the blast radius
- Flagging Medium/Low CVEs with the same urgency as Critical/High
- Missing Docker base image versions as a dependency surface
