# PR #56: Zod compatibility and remaining upstream risk

Reviewed 2026-10-30 against Remotion **4.0.522**, installed Zod **4.6.6**,
and the review on [PR #56](https://github.com/urfavxbf/video-ai-editor/pull/56).
This remains a **partial mitigation**. Keep issue #54 P1 #2 unchecked until
the bundled-code problem is resolved or the owner explicitly accepts the risk.

## Why the version warning remains

The CLI prints:

```text
Version mismatch:
Extra packages with wrong versions:
  - zod: installed 4.6.6, required 4.5.4
```

`@remotion/cli/dist/extra-packages.js` declares an exact Zod version.
`versions.js` compares the installed version with that string, rather than
running a compatibility test. This warning is real and must remain visible;
we have not changed package metadata, hidden it, or reinstated vulnerable Zod.

The limited rationale for retaining the override on this unmerged branch is
that 4.6.6 repairs the installed dependency's collection preflight behavior,
while the representative checks below pass without changing any Remotion pin.
That is evidence for a temporary compatibility exception, not upstream
certification or acceptance of production risk. Successful fixture rendering
alone is insufficient evidence for the editor's other paths.

## Checks and their limits

Run `node --test tests/zod-compatibility.test.cjs`. These eight bounded tests
also run in the existing PR safety gate:

- Oversized arrays, sets and maps fail before visiting elements; valid inputs
  succeed. Three-element inputs suffice; no memory-exhaustion test is needed.
- Studio's actual prop-schema inference accepts current hero-stage defaults
  and numeric chapter changes, and rejects an invalid chapter type.
- Schema helpers traverse nested enum/array props used by prop serialization.
- Composition drag data round-trips through the installed `zod/mini` path;
  malformed JSON and traversal paths are rejected.
- Both published protocol module formats round-trip valid Element payloads
  and reject malformed versions and 101 dependencies. **Final rejection does
  not establish preflight rejection inside these bundled parsers.**

The tests deliberately exercise private Studio helpers against the pinned
release; review those paths when changing Remotion versions. They do not
replace real browser testing or exercise every schema/editor extension.

Additional local Chromium checks against the actual Studio server covered
PixelProductionProof preview, stepping, play/pause, switching to
HeroCharacterStage with both approved images, and changing the render modal's
transient chapter prop from 1 to 2 in JSON and observing it in the Schema tab.
No uncaught browser page errors occurred.
No source-backed save, third-party Element installation, paid/licensed flow,
or arbitrary user project was exercised. Existing CLI/CI fixture exports,
77 Python tests, asset verification and typechecking remain separate checks.

## Embedded code is unaffected by the npm override

Published `@remotion/studio-protocol` CJS/ESM bundles and Studio's ESM bundles
contain Zod 4.5.4 implementations. They allocate/traverse collection results
before applying maximum-size checks. The npm override changes the separately
installed package; it cannot replace code already bundled into Remotion.

A bounded probe of the unchanged protocol implementation with 101 dependencies
confirmed allocation before rejection at a maximum of 100. This demonstrates
the vulnerable parsing order, not production memory exhaustion. A clean
`npm audit` reports installed dependency advisories, not those embedded copies.

Relevant entry-path protections were inspected and locally probed:

- The HTTP install handler limits body size to **1,000,000 bytes before JSON
  parsing**. One just-over-limit request returned 413; a malformed protocol envelope
  input returned 400, and a non-loopback HTTP origin returned 403.
- The HTTP origin policy accepts **any HTTPS origin** and loopback HTTP.
  It is not a trusted-site allowlist or authentication boundary.
- The browser message handler checks the actual installed Element-library
  iframe's `contentWindow` and an allowed origin before parsing. Its origin
  predicate also accepts HTTPS generally. We did not load a third-party
  library or establish an equivalent byte-size cap for structured messages.
- Element payload creation explicitly bounds dependency count. Incoming
  parsing still reaches the embedded code; an eventual payload-size check is
  not equivalent to a check before allocating/traversing collections.

Thus an unbounded unauthenticated HTTP-server DoS has **not** been established,
but neither body limits nor origin checks justify declaring the embedded
advisory fixed. Keep Studio local and avoid untrusted Element libraries while
this remains unresolved; these precautions do not repair the bundled code.

## Preferred upstream-compatible resolution

Registry inspection found the latest published Remotion release to be
**4.0.539**. Its media, Studio, Studio server and protocol packages still
declare Zod 4.5.4. The downloaded protocol tarball also still embeds that
version and the allocation-before-check implementation. Merely upgrading to
this release would not resolve the finding and is not proposed here.

The preferred resolution is an upstream coordinated release that:

1. Declares a patched Zod version in every affected package and the CLI's
   expected-version table.
2. Rebuilds all protocol and Studio bundles against the patched implementation.
3. Applies preflight collection/payload limits at untrusted ingress, including
   iframe messages, then validates both valid and rejected inputs.
4. Passes this compatibility suite, actual editor flows and the production
   fixture gate before all Remotion pins move together in a separate change.

There is currently no verified fully upstream-compatible remediation that
retains 4.0.522 unchanged. Do not suppress the warning, spoof dependency
versions, downgrade Zod, use `npm audit fix --force`, or introduce an ad-hoc
vendor patch merely to make this PR look complete. If an upstream release is
unavailable, a narrowly reviewed vendor patch/rebuild is a separate decision
requiring its own reproducible tests and maintenance plan. No upstream report
was sent as part of this review; the blocker is tracked in PR #56 and issue #54.
