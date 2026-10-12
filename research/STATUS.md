# Project Status

Last updated: 2026-10-12

## Confirmed repository state

- Repository: `ADHHHD-Thingz/ECU-Definition-Database`
- Default branch: `main`
- Starting commit: `d0a061f0de77e8576eec61b00f8e82bf3d437894`
- Starting repository content: README only; no tracked corpus or tooling.
- Work branch: `project/ecu-definition-recovery`

## Prior analysis available

A prior conversation extraction report and `map_index.csv` are present in conversation files. The report described MazdaEdit v3 and SubaruEdit v1 archives and explicitly warned that encoded `eattributes` had not been decrypted. Those outputs are useful leads but need to be tied to source archive hashes and reproducibly regenerated before they become authoritative project data.

Reported historical counts (not yet re-verified here):
| Input | XML files | Maps | `eattributes` |
|---|---:|---:|---:|
| MazdaEdit v3 | 1,697 | 172,470 | 237,985 |
| SubaruEdit v1 | 65 | 8,557 | 18,035 |

## Work completed in this branch

- Added project charter and staged work plan.
- Added persistent agent instructions.
- Added a non-destructive file inventory/parser audit tool.
- Added automated CI and a weekly/manual inventory workflow.

## First technical findings

- The repository does not yet contain the original archive inputs, so archive-level counts cannot currently be reproduced from this repository.
- The public SubaruDefs comparison must be pinned to an exact upstream revision before match claims are promoted.
- Prior family-level candidate associations are leads only, not exact ROM or definition matches.
- Opaque `eattributes` are to remain opaque until a validated decoding path or known plaintext comparison proves their meaning.

## Blockers

1. Add or make available the original authorized MazdaEdit v3 and SubaruEdit v1 archives, or an existing extracted corpus and source hashes.
2. Identify an authorized unencrypted Subaru XML example for schema comparison if one is available.
3. Confirm which BIN/ROM sources may be indexed and redistributed. Hashing and local matching are separate from redistribution permission.

## Next tasks

1. Run the new audit against repository contents in CI.
2. Add tests and schema for the normalized database.
3. Pin SubaruDefs revision and inventory its public definition files.
4. Generate match reports separating exact matches from family-level candidates.
5. Revisit opaque payload analysis only after structural baselines and known examples exist.