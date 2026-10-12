# ECU Definition Recovery & Validation Project

## Objective

Build a reproducible, evidence-backed database of ECU definition files and ROM associations. Preserve original artifacts, identify duplicates and coverage gaps, compare equivalent definitions across formats, and only promote reverse-engineered interpretations when evidence supports them.

## Operating rules

1. **No hallucinated facts.** Every technical claim must have a source path, URL, ROM hash, disassembly reference, test, or clearly marked hypothesis.
2. **Preserve originals.** Never silently overwrite, rename, normalize in place, or delete source files. Use derived outputs and explicit change logs.
3. **Separate metadata from recovered payloads.** A map label or encoded `eattributes` blob is not proof that axis/data values have been decoded.
4. **Match by evidence, not names alone.** Prefer ROM ID, file hash, ROM size, addresses, dimensions, storage type, endianness, scaling, axis signatures, and cross-reference evidence.
5. **Confidence is explicit.** Use `confirmed`, `strong_candidate`, `candidate`, `hypothesis`, or `unresolved`; state why.
6. **Provenance is mandatory.** Record source URL/path, retrieval date, SHA-256 where applicable, license/usage notes, transformation steps, and evidence links.
7. **Keep the main branch stable.** Work on feature branches and open a PR for review. Do not commit large ROM binaries or proprietary archives without explicit repository policy approval.
8. **Respect access controls and licensing.** Research public sources and authorized local artifacts. Do not bypass authentication, licensing, or access controls.
9. **Reproducibility first.** Prefer scripts, tests, deterministic output, caches, and compact reports over manual one-off edits.
10. **Do not overstate completion.** A successful XML parse is not proof of semantic correctness or successful decryption.

## Initial scope

- MazdaEdit v3 and SubaruEdit v1 XML definition extraction and comparison.
- Public Subaru definitions, particularly SubaruDefs/ECUFlash and RomRaider sources.
- Definition formats: XML, XDF, KP, A2L, JSON, CSV, SQLite and related metadata.
- ROM/BIN associations and ROM-ID matching.
- Honda OBD0/OBD1 and other ECU families can be added as separately tracked corpus workstreams; do not let them obscure the first Subaru/Mazda baseline.

## Work stages

### Stage 0 — Project controls
- [x] Create a feature branch and project instructions.
- [x] Add a non-destructive definition inventory/audit tool.
- [x] Add CI and scheduled inventory workflow.
- [ ] Establish source-artifact manifest and license/provenance fields.
- [ ] Record the first reproducible baseline report.

### Stage 1 — Source intake and integrity
- [ ] Inventory all tracked files and available archive inputs.
- [ ] Hash each artifact; identify exact duplicates and likely duplicate variants.
- [ ] Parse supported text formats without dropping unknown fields.
- [ ] Record parse failures rather than silently skipping them.

### Stage 2 — Canonical data model
- [ ] Design normalized SQLite schema with raw-record preservation.
- [ ] Store source artifacts, ECU/vehicle/ROM identities, definition records, axes, scaling, relationships, evidence and validation results.
- [ ] Keep opaque/encrypted payloads as opaque values until a decoding path is proven.
- [ ] Add migration and schema tests.

### Stage 3 — Subaru/Mazda cross-reference
- [ ] Acquire and pin a public SubaruDefs source revision.
- [ ] Inventory ECUFlash and RomRaider definitions and metadata.
- [ ] Match at ROM/definition level; family-name similarity alone is insufficient.
- [ ] Produce matched, candidate, unmatched, and conflict reports.
- [ ] Incorporate authorized unencrypted examples for structural comparisons.

### Stage 4 — ROM association and validation
- [ ] Match available BINs using ROM ID, size, hashes, known IDs and validated addresses.
- [ ] Keep raw ROM bytes separate from inferred metadata.
- [ ] Validate map address, size, dimensions, type, endian, scaling and axis definitions independently.
- [ ] Add automated tests for every promoted claim.

### Stage 5 — Targeted reverse engineering
- [ ] Prioritize unresolved items by coverage impact and evidence availability.
- [ ] Trace decoder/loader logic only where definitions remain blocked.
- [ ] Compare decoded candidate payloads against independent unencrypted definitions.
- [ ] Record exact transformation steps and reproducible test vectors.

### Stage 6 — Release
- [ ] Generate coverage dashboards and missing-definition lists.
- [ ] Publish reproducible database/export artifacts with provenance.
- [ ] Review redistribution rights before publishing source artifacts or decoded content.

## Current baseline

The repository initially contained only a short README and no tracked definition corpus. Prior analysis artifacts are available in the ChatGPT conversation/library, but the original MazdaEdit/SubaruEdit archives and prior SQLite bundle have not yet been confirmed in this repository. The previously reported counts are historical starting points, not re-verified by this repository's current CI.

Historical extraction figures to verify against the original inputs:
- MazdaEdit v3: 1,697 XML files, 172,470 `<map>` elements, 237,985 `eattributes` elements.
- SubaruEdit v1: 65 XML files, 8,557 `<map>` elements, 18,035 `eattributes` elements.

## Definition of done

A work item is complete only when its output is reproducible, source provenance is recorded, uncertainty is explicit, tests pass, and a reviewer can trace the conclusion to evidence.