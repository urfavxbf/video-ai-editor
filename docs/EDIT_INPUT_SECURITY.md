# Edit input security (#68)

`src/compositionMetadata.ts` is the shared runtime contract for metadata and
render frames. It rejects unknown keys/effects, unsafe local path syntax,
unsupported extensions, invalid geometry, source overruns, non-finite audio
gains (allowed 0–2), invalid trims, >3000 cuts and >108000 timeline frames.
All 21 registered effects and the checked-in 299-frame edit remain supported.
This stays independent of the pending Zod PR #56.

Use `node scripts/validate-edit.cjs spec.json --media` before rendering supplied
footage. The contract runs first; the optional physical preflight restricts
FFprobe to existing files under public/{sample,takes,voiceovers,audio,music},
rejects symlinks/remote inputs, limits file size to 2 GiB and duration to one
hour, restricts protocols to file, bounds probing to 15 seconds per file, and
checks measured video/audio/trim bounds and effect derivative frames. The overall
CLI preflight is limited to 120 seconds. Studio metadata validates syntax only;
file existence requires this local preflight. The committed sample media are
intentionally ignored and must be generated locally with `npm run sample`.
Do not serve untrusted symlink trees from public/; do not mutate media during a
preflight/render job. Media paths remain public assets when served by Remotion.

## Exposure audit performed 2026-10-31

`python3 scripts/audit-media-exposure.py` fetched/scanned reachable branch/tag
history (non-shallow checkout). It reports paths, blob IDs and counts, never URLs
or credential values. The heuristic found no signed URLs in current tracked
files and one historical blob version of
`render-queue/dudut-20261027-premium.json`. Binary/large blobs >4 MiB are outside
this scan. Token validity was not tested and cannot be assumed revoked/expired.
The historical download capability should be invalidated at its source if still
active; owner authorization is required for token revocation or storage rotation.
No history rewriting or secret rotation was performed.

Active deployment exposure remains unverified: the GitHub connector rejects the
deployment endpoint and the managed CLI receives `Forbidden`. Do not treat this
as a clean deployment audit. The owner should inspect any active deployments
and artifacts for historical queue contents before considering exposure closed.

Keep future media URLs out of queue JSON, commits and logs. Use short-lived,
scoped URLs injected through a secret manager only for explicitly authorized
fetch jobs; prefer authenticated private object storage and access-controlled
artifacts for confidential inputs. Removing a current file never erases history.

Validation: TypeScript, 23 Node contract/duration/episode tests, 81 Python tests,
actual Chromium metadata checks, existing fixture render/probe safety gate.
