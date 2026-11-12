# Security policy

This policy covers every public repo in [byo-oss](https://github.com/byo-oss) that has no `SECURITY.md` of its own, for example `core`, `notifications`, `support`, `entitlements`, `mailer`, `conventions` and `site`. It applies to the published packages `@byo-oss/core`, `@byo-oss/notifications`, `@byo-oss/support`, `@byo-oss/entitlements` and `@byo-oss/mailer`.

BYO is a small independent project, not affiliated with the better-auth team.

## Supported versions

Every package is still `0.x`. Only the latest minor of each package gets security fixes.

In `0.x`, a new minor can be breaking, so we do not backport. A fix goes into the next release of the package (a new minor when it narrows a peer range). Upgrade to the latest release of the package to get it. Releases are published from CI with npm provenance. The [conventions](https://github.com/byo-oss/conventions/blob/main/SPEC.md) describe how versions and releases work.

## Report a vulnerability

Report privately. Do not open a public issue, pull request or discussion for a vulnerability.

1. Open the Security tab of the affected repo, for example [github.com/byo-oss/support/security](https://github.com/byo-oss/support/security).
2. Click **Report a vulnerability**.
3. Fill in the form.

If you are not sure which repo is affected, use `core`.

A good report has:

- The package and version.
- The better-auth version and database adapter you tested with.
- What the vulnerability is and what an attacker gains.
- Steps to reproduce, ideally a minimal script or test.
- Any fix you suggest.

## What to expect

- We acknowledge your report within a few days.
- We tell you whether we accept it as a vulnerability, and why if we do not.
- If we accept it, we work on a fix in the private advisory and release it. We credit you in the advisory if you want that.
- We publish the advisory once a fixed version is on npm.

There is no SLA beyond the rule for dependencies below. We are a small team and will not promise dates we cannot keep. We will keep you updated.

## Vulnerabilities in a dependency

A bug in a package we depend on, such as `better-auth` or `@better-auth/*`, is that project's to disclose and fix. An advisory here is a GitHub advisory, in the global database or the upstream repository, or a CVE. It counts as published when the first of those appears. When one affects a version that a BYO package's `peerDependencies` or `dependencies` range admits, including one pinned inside a direct dependency:

- We narrow that range so it admits no affected version, and release.
- We release within 7 days, or within 72 hours when GitHub rates the advisory critical, counted from the later of the advisory's publication and the fixed version's release.
- If the fixed version needs code changes that can't ship in that window, we say so in the package's README and an issue within the window, and release as soon as we can.
- The release notes (the package's upgrade notes and its GitHub release) name the advisory, or link the upstream notice that lists it.
- An optional peer that only a `./testing` export uses (vitest) is exempt from these windows. Its floor rises in the package's next minor release.
- Older minors whose range still admits an affected version (test peers aside) are deprecated on npm. The deprecation message names the advisory and the BYO release that raised the floor.

We do not file our own GitHub advisory for a bug in a dependency. Follow the upstream advisory, and use the deprecation message to find the BYO version to upgrade to. A BYO bug that makes an upstream bug exploitable is ours, and gets an advisory of its own.

If you find a bug in a dependency, report it to that project first. Tell us too if BYO code makes it worse.

## Scope

In scope: the code in the repos above and the packages published from them.

Out of scope: bugs that need a compromised app, database or server; bugs in better-auth or another dependency itself; and your own app's configuration.
