<!-- SPDX-License-Identifier: Apache-2.0 -->
# Additive superset merge and historical code-loss policy

Status: proposed governance rule, 2026-11-18. This file is an original
Apache-2.0 governance document, not a claim that the repository's upstream
code or all its files have become Apache-2.0.

## Binding merge invariant

Preserve the supported upstream API/ABI/behavior **and** every previously
accepted fork-specific capability, performance contract and regression test.
Select the strongest *verified compatible* atoms additively, based on
correctness, measured performance, allocation, native memory, maintainability
and legal provenance. Keep provider-specific public interfaces and their
null/equality/order/threading/serialization/lifecycle/JNI contracts.
Disagreements require an explicit compatibility decision, not code deletion.
Do not turn an optimized fork into an upstream-only replacement.

Atomize by semantic leaf; classify logic, structural and fuzzy hash matches as
candidates only. Hash equality never substitutes for API, behavioral,
compiler, runtime and regression proof. Keep one semantic owner and
adapters where possible; do not silently move, delete, merge, rename or
relicense existing implementations.

## Mandatory full-history and PR check *before* change approval

Pin default head and donor revisions. Enumerate all discoverable branches,
tags, remote refs and open/closed/merged/unmerged PRs, with complete pagination
and explicit coverage. Traverse every *reachable* ancestral commit back to
the earliest available root on every discoverable ref, including first-parent
and side-branch/merge paths. Inspect historical PR diffs, discarded side
changes, upstream syncs, reverts, squash/cherry-pick candidates and
deleted/overwritten code. Compare prior APIs, accepted extensions and tests
to the proposed combined tree.

Record evidence-backed `CANDIDATE_LOSS` / `CANDIDATE_REGRESSION` /
`SUPERSEDED_VERIFIED` / `RESTORED` / `NOT_VERIFIED`. A deleted line or
hash mismatch alone is not proven behavioral loss. Unreachable or unavailable
historic objects cannot be asserted recovered: report that limitation and
fail closed for claims requiring them.

Do not treat a tip-only sample as a full audit. For each run capture
`inventory_observed_at_utc`, `history_last_attempted_at_utc`,
`history_last_verified_at_utc` (only on exhaustive verified coverage),
pinned head SHA, earliest reachable SHA, scanned/total refs and PRs,
coverage gaps, checkpoint cursor, exact proof SHA, evidence URI and
last verified gate. `NOT_RUN` and `PARTIAL` must be explicit. Archive
old checkpoints and invalidate the claim for a new head until rescanned.
Canonical estate-level history/checkpoint custody is private Synexia;
result-only product forks must not acquire private recipe engines or bulky
qualification bundles. Local repository instruction files remain in force.

## Licensing is per-file, never blanket

Prefer genuine unmodified Apache-2.0 for **owned, eligible new work**.
Preserve donor copyright, SPDX, LICENSE, NOTICE, patent and attribution
obligations. Apache-inspired variants require separate compatibility review.
MIT/BSD-style code is considered only with its notices and permitted terms;
GPLv2-only/OpenJDK, GPLv3, other copyleft, commercial, unlicensed and unknown
sources need target-specific clearance. Do not declare an entire fork Apache
merely because new original code is Apache-2.0.

Algorithms and ideas are generally outside copyright, but protected source
expression is not; patents, trade secrets and agreements also matter.
An LLM rewrite or atom/pattern transform **does not erase source copyright**
or establish independent provenance. If donation is legally unavailable,
derive an original implementation from lawfully obtained functional
specifications, independently designed algorithms and independent tests,
then verify provenance before admitting it.

## MOP SDK: source-bound atoms and bidirectional pattern composition

For source changes, inherit the [canonical Synexia universal atom/pattern invariant](https://github.com/hsoliwal/com.synexia/blob/develop/docs/M3-SCALE/invariants/SYNEXIA-UNIVERSAL-API-ATOM-PATTERN-EVOLUTION-1.md) and [historical additive superset law](https://github.com/hsoliwal/com.synexia/blob/develop/docs/M3-SCALE/invariants/SYNEXIA-ADDITIVE-MERGE-FULL-HISTORY-20261118.md). The canonical repository owns reusable Maven/OpenRewrite recipes, proof ledgers and correction history; this catalogue fork does not acquire those private engines.

**Downward:** repository -> project -> module -> package/namespace -> file -> types/interfaces, fields, methods, exports, comments and meaningful semantic atoms. Preserve its actual format and language semantics; this repository is primarily a data-driven documentation catalogue, not a Java-only product. Source, build templates, generated Markdown and upstream content have distinct owners and licenses.

**Upward:** verified atoms -> file composition -> package/interface contracts -> modules -> project -> repository/SDK. Record contracts, effects, pattern roles, caller dependencies, source-hash and normalization-version identities, NO_SAFE_EXTRACTION/UNRESOLVED decisions, and explicit proof obligations. Recompute only the affected dependency closure; never force tiny helpers or change supported APIs by style.

**Evidence:** independent files may be inventoried and prepared in bounded parallel, but each mutable file has one writer; verified promotion is deterministic and serial. LogicHash, StructuralHash, SimHash and labels identify comparison candidates only. Maintain source-bound documentation as persistent machine memory; independently validate a best-qualified implementation under measured constraints, not an asserted universal optimum. Preserve any generated-page/template workflow and exact upstream attribution. Do not replace accepted code or rewrite upstream licensing via LLM paraphrase. Missing compiler, tests, full history, format/renderer verification or provenance remains NOT_RUN/HOLD.

**Enrollment status:** this is governance-only. It does not claim a full Git/PR history audit, source atomization, semantic equivalence, regenerated catalogue, CI or runtime validation.

### Registered algorithms, patterns and machine-tagged unknowns

For every proposed change, consult the authorized, versioned algorithm/operator/pattern catalogue first. A known pattern or algorithm requires a stable ID, applicability rules, roles, contracts, effects and an evidence-scoped status. A structural resemblance, LogicHash/SimHash candidate or LLM suggestion is not an admitted known pattern. Preserve unknowns as `UNKNOWN_ALGORITHM`, `UNKNOWN_PATTERN` or `UNPROVEN_MATCH` in the existing machine-readable source inventory, with source pin, owner, atom ID, dependencies, rationale, proof state and review owner. Link those records from accurate documentation or existing supported annotations; never invent noncompiling annotations or arbitrarily rewrite the source. Repeated unknowns become pattern proposals only after an independent recognizer, validator, template, provenance review and qualification. No unknown tag authorizes code replacement, license change or merge. Canonical proposed extension: [Synexia MOP SDK lattice PR #18784](https://github.com/hsoliwal/com.synexia/pull/18784).

## Admission order

Inventory -> full available history/PR audit -> compatible superset design
and exact diff proposal -> explicit change authorization -> patch/hash ->
lint/static analysis -> compile -> targeted tests -> broader tests ->
native/JNI/runtime/product verification -> PR review and head-drift gate ->
post-merge preservation check and durable last-verified checkpoint.

Fail closed on source loss, unproven equivalence, head drift, rights uncertainty,
skipped gates or missing receipts. Do not force-push, rewrite public ancestry,
or silently restore a historical version without reviewing present callers.

**Execution status:** Policy recorded as a proposal; an inception-to-tip
history audit and repository-specific `last_verified` are NOT_RUN unless an
independent durable checkpoint explicitly proves otherwise.

License references: https://www.apache.org/licenses/LICENSE-2.0 ;
https://www.apache.org/foundation/license-faq ;
https://www.copyright.gov/circs/circ61.pdf .
