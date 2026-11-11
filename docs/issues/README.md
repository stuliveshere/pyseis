# pyseis design issues

Working set of design issues for the agent-friendly redesign of pyseis, now tracked as GitHub issues #79–#117. Background: [`../agent-forward-software-research.md`](../agent-forward-software-research.md) and [`../agent-friendly-recommendations.md`](../agent-friendly-recommendations.md).

**How to use this:**

- Design decisions were made in the 2026-11-11 sessions; see the register below. Each decision is **Open**, **Proposed**, **Agreed** (including *Settled* by another decision) or **Deferred**.
- **Build** in the phase order below. Hotfixes (H01–H14) land on the current code before any redesign work.
- The issue text now lives on GitHub. This page is a snapshot of the register as of 2026-11-11; when a decision changes, update the GitHub issue and this table.

## Issues

| Issue | Title | Status | Depends on |
|---|---|---|---|
| [000](https://github.com/stuliveshere/pyseis/issues/79) | Storage architecture: Parquet trace tables (Zarr/MDIO hypercubes deferred) | Agreed (2026-11-11 voice session); D000.8 deferred to F01 | none (foundation) |
| [001](https://github.com/stuliveshere/pyseis/issues/80) | Define dataset metadata contract, canonical header vocabulary, units and CRS | Agreed (2026-11-11 voice session); D001.9 deferred to F04 | 000 |
| [002](https://github.com/stuliveshere/pyseis/issues/81) | Parallel streaming ingest in input order | Agreed (2026-11-11 voice session) | 000 (layout, keys), 001 (contract, vocabulary), 005 (errors, logs), 015 (read/flow/write model) |
| [003](https://github.com/stuliveshere/pyseis/issues/82) | Establish a clean test baseline (tests on demand) | Agreed (2026-11-11 voice session) | none (do first) |
| [004](https://github.com/stuliveshere/pyseis/issues/83) | Data-correctness hotfixes on the current code (umbrella) | Agreed (2026-11-11 voice session) | 003 (test baseline) |
| [005](https://github.com/stuliveshere/pyseis/issues/84) | Errors, warnings, provenance and logs | Agreed (2026-11-11 voice session) | none. Lands before 001/002 implementation so new code uses it. |
| [006](https://github.com/stuliveshere/pyseis/issues/85) | `SeismicDataset`: manifest-backed, streaming dataset API | Agreed (2026-11-11 voice session) | 000, 001, 002, 005, 015, 016 |
| [007](https://github.com/stuliveshere/pyseis/issues/86) | Exporters for multi-part datasets (SEG-Y, SU, SEG-D, GeoPackage) | Agreed (2026-11-11 voice session) | 001, 006, 008 |
| [008](https://github.com/stuliveshere/pyseis/issues/87) | Views and declared sort orders | Agreed (2026-11-11 voice session) | 000 §E (design), 002, 005, 006, 016 |
| [009](https://github.com/stuliveshere/pyseis/issues/88) | Header overlays (edits without rewriting base headers) | Agreed (2026-11-11 voice session) | 000 (D000.5), 006, 008, 016 (versions and branches) |
| [010](https://github.com/stuliveshere/pyseis/issues/89) | Compaction, re-sort and repartition | Agreed (2026-11-11 voice session) | 000, 006, 008, 016 |
| [011](https://github.com/stuliveshere/pyseis/issues/90) | `describe` and `inspect`: structured summaries, levels and return-message rules | Agreed (2026-11-11 voice session) | 001, 002 (pre-flight probe), 005 (results, logs), 006 |
| [012](https://github.com/stuliveshere/pyseis/issues/91) | Command-line interface | Agreed (2026-11-11 voice session) | 005, 006, 011, 019 (and the issues behind each command) |
| [013](https://github.com/stuliveshere/pyseis/issues/92) | AGENTS.md, documentation rewrite, tested examples and schema reference | Agreed (2026-11-11 voice session) | 001 (vocabulary), 000/006/016/019 (API). The `AGENTS.md` terminology section can land immediately. |
| [014](https://github.com/stuliveshere/pyseis/issues/93) | Packaging, dependencies, Python version and versioning | Agreed (2026-11-11 voice session) | none (dependency and package-data fixes can be done early); version bump with the redesign |
| [015](https://github.com/stuliveshere/pyseis/issues/94) | Unified read → flow → write model | Agreed (2026-11-11 voice session) | 000, 001, 006 |
| [016](https://github.com/stuliveshere/pyseis/issues/95) | Dataset versions and branches | Agreed (2026-11-11 voice session) | 000 (manifest, atomic commits) |
| [017](https://github.com/stuliveshere/pyseis/issues/96) | Cleanup and retention | Agreed (2026-11-11 voice session) | 016 (versions) |
| [018](https://github.com/stuliveshere/pyseis/issues/97) | Projects, pack and archive | Agreed (2026-11-11 voice session) | 000, 016 |
| [019](https://github.com/stuliveshere/pyseis/issues/98) | Flows and execution (modules, flow files, Dask) | Agreed (2026-11-11 voice session) | 005, 006, 015 |
| [H01](https://github.com/stuliveshere/pyseis/issues/104) | H01: Sample interval silently defaults to 2 ms (dataset and writer) | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H02](https://github.com/stuliveshere/pyseis/issues/105) | H02: SEG-D sample interval defaults to 2000 µs when `base_scan_interval` is 0 | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H03](https://github.com/stuliveshere/pyseis/issues/106) | H03: SEG-Y exporter guesses sample-interval units and falls back to 4 ms | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H04](https://github.com/stuliveshere/pyseis/issues/107) | H04: SEG-D exporter falls back to 2 ms | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H05](https://github.com/stuliveshere/pyseis/issues/108) | H05: Viewer falls back to 4 ms and defaults `group_by` to a non-existent column | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H06](https://github.com/stuliveshere/pyseis/issues/109) | H06: SEG-D reader silently drops aux channel set 1 | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H07](https://github.com/stuliveshere/pyseis/issues/110) | H07: SEG-Y reader silently zero-pads short traces | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H08](https://github.com/stuliveshere/pyseis/issues/111) | H08: Unknown or misspelled `custom_mappings` keys are silently dropped | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H09](https://github.com/stuliveshere/pyseis/issues/112) | H09: Remove ignored `header_def` and `mapping_path` arguments from `SEGYExporter` | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H10](https://github.com/stuliveshere/pyseis/issues/113) | H10: Warnings printed to stdout | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H11](https://github.com/stuliveshere/pyseis/issues/114) | H11: Docs use non-existent columns `source_id` and `cdp_id` | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H12](https://github.com/stuliveshere/pyseis/issues/115) | H12: Docs reference non-existent `to_parquet_buffer()` | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H13](https://github.com/stuliveshere/pyseis/issues/116) | H13: Docs claim `filter()` uses predicate pushdown | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [H14](https://github.com/stuliveshere/pyseis/issues/117) | H14: Unused `chunk_size` parameter on importers | Agreed (hotfix on the current code, before any redesign work) | 003 (test baseline) |
| [F01](https://github.com/stuliveshere/pyseis/issues/99) | Feature request: Zarr/MDIO hypercubes for regularised, chunk-parallel processing | Deferred. Revisit when pyseis needs random-write parallel processing (MPI/Dask), time slices or volume work. | — |
| [F02](https://github.com/stuliveshere/pyseis/issues/100) | Feature request: preview tables for fast viewing and agent visual QC | Deferred | 000, 006 |
| [F03](https://github.com/stuliveshere/pyseis/issues/101) | Feature request: MCP server for pyseis | Deferred. Revisit when agents need pyseis from clients without shell access, or for shared, authenticated access to datasets. | — |
| [F04](https://github.com/stuliveshere/pyseis/issues/102) | Feature request: custom/local CRS grids and reading the CRS from input files | Deferred | 001 |
| [F05](https://github.com/stuliveshere/pyseis/issues/103) | Feature request: Dask on clusters | Deferred | 019 |

## Build order

- **Phase 0: baseline:** 003
- **Phase 1: hotfixes on the current code (before any redesign):** 004 (H01–H14)
- **Phase 2: groundwork:** 005, 014, 013 (AGENTS.md terminology section only)
- **Phase 3: contract:** 001
- **Phase 4: format foundation:** 000, 016, 006, 015, 002
- **Phase 5: using the format:** 019, 008, 007, 011, 012
- **Phase 6: documentation:** 013 (full)
- **Phase 7: dataset management:** 009, 010, 017, 018
- **Deferred:** F01, F02, F03, F04, F05

Hotfixes come first because current behaviour produces wrong data. The CLI, `describe()` and exporters come after the format foundation so they're built once, on the new layout.

## Decision register

Totals: Open 1, Proposed 0, Agreed 78, Deferred 3

### Open: need a decision

| ID | Issue | Question | Recommendation |
|---|---|---|---|
| D019.5 | [019](https://github.com/stuliveshere/pyseis/issues/98) | Flow file details (exact YAML schema, expression language for selects) | To be designed when implementing |

### Proposed: confirm or change

_None._

### Agreed

| ID | Issue | Decision | Notes |
|---|---|---|---|
| D000.1 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Parquet now as the system of record; Zarr hypercubes with an explicit bin/regularise boundary deferred to F01 |  |
| D000.2 | [000](https://github.com/stuliveshere/pyseis/issues/79) | A dataset is always a `dataset.json` manifest plus one or more parts, the same layout for one part or many; no footer-manifest special case. A standalone single Parquet file exists only as a `pack` export |  |
| D000.3 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Separate, row-aligned header and data parts |  |
| D000.4 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Physical layout is always generic (write/input order, `trace_id`). Parts follow input files (for SEG-D, one per gather) or trace ranges, with an optional `split_on` hint. Semantic sort order (primary/secondary/tertiary + `partition_by`) is nullable metadata, set at ingest or later, verified against headers, failing noisily on violation (§E) |  |
| D000.5 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Base headers immutable; edits as overlays keyed by `trace_id`. Overlays never change physical order |  |
| D000.6 | [000](https://github.com/stuliveshere/pyseis/issues/79) | One data table for all traces including aux (flagged by `trace_code`). Record-length mismatch fails noisily, with options to pad to the longest record or to a set length (true length in `trace_num_samples`). Sample-interval mismatch fails noisily, with an option to resample to the finest interval (recorded in provenance). Appending longer data than the table fails clearly |  |
| D000.7 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Manifest: our own minimal `dataset.json`, designed to map onto Delta Lake/Iceberg/lakeFS later |  |
| D000.9 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Default when no order given: generic keys plus suggestions; `sort_order="suggested"` as explicit opt-in; never inferred silently |  |
| D000.10 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Duplicate full key tuples fail by default (`allow_duplicates` to opt out) |  |
| D000.11 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Terminology: primary / secondary / tertiary keys with `partition_by` |  |
| D000.12 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Header-only **views** (renamed from "indexes") for alternative orders, stored under `views/`; a full re-sort writes a new dataset |  |
| D000.13 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Per-part headers are authoritative; an optional survey-wide header table is a derived cache, tied to the version it was built from |  |
| D000.14 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Dataset directories named `<name>.pyseis` (e.g. `line12.pyseis`), never a bare `.pyseis` (hidden on Linux) |  |
| D001.1 | [001](https://github.com/stuliveshere/pyseis/issues/80) | Canonical column naming | Descriptive snake_case with ProMAX/SEG-Y/SU names as `aliases`. SEG-D `.map.yaml` files keep ProMAX names on the left-hand side for the Java SeisSpace plugin; pyseis translates through the aliases |
| D001.2 | [001](https://github.com/stuliveshere/pyseis/issues/80) | Unit conventions | Times in ms, everything else SI; real floats with unit metadata, no integer + scalar; sample interval integer µs; absolute times epoch ms UTC |
| D001.3 | [001](https://github.com/stuliveshere/pyseis/issues/80) | Missing sample interval | Fail noisily. Options: supply manually (also when the file value is wrong; original kept in provenance), or explicitly import as unknown, in which case time-based operations refuse to run |
| D001.4 | [001](https://github.com/stuliveshere/pyseis/issues/80) | Missing CRS | Recorded as unknown with a warning; never assume a datum |
| D001.5 | [001](https://github.com/stuliveshere/pyseis/issues/80) | CRS representation | String: EPSG code or "unknown", plus a readable name; horizontal and vertical separate. WKT and custom grids deferred (F04) |
| D001.6 | [001](https://github.com/stuliveshere/pyseis/issues/80) | Column units and descriptions | Optional for all columns: give a unit, mark dimensionless, or leave unknown; no warning, no special handling |
| D001.7 | [001](https://github.com/stuliveshere/pyseis/issues/80) | Per-trace sample column names | `trace_sample_interval_us`, `trace_num_samples` |
| D001.8 | [001](https://github.com/stuliveshere/pyseis/issues/80) | Where the contract lives | `dataset.json`; each part's footer carries the contract version and dataset id |
| D002.1 | [002](https://github.com/stuliveshere/pyseis/issues/81) | Input order | The order of the file list given to ingest. Natural filename order is the default of the list-building helpers, not of ingest. The final order is recorded in the manifest |
| D002.2 | [002](https://github.com/stuliveshere/pyseis/issues/81) | Parallel execution | Self-contained per-part workers run by a pluggable executor; default Dask local cluster on a single workstation or laptop (revised by 019); clusters deferred (F05) |
| D002.3 | [002](https://github.com/stuliveshere/pyseis/issues/81) | Small inputs | Always one part per input file; no grouping at ingest. Merge small parts afterwards with `compact` (010) |
| D002.4 | [002](https://github.com/stuliveshere/pyseis/issues/81) | Splitting large single inputs | By size by default, or at changes of a `split_on` header; neither asserts an order |
| D002.5 | [002](https://github.com/stuliveshere/pyseis/issues/81) | Mismatched sample count or interval across inputs | Settled by D000.6: fail noisily; pad (longest or set length) / resample to finest as options |
| D002.6 | [002](https://github.com/stuliveshere/pyseis/issues/81) | Short traces | Settled by D000.6: fail noisily; padding options record the true length per trace |
| D002.7 | [002](https://github.com/stuliveshere/pyseis/issues/81) | Input discovery | Ingest only takes a file list (Python list, CLI paths or list file); separate helpers build lists from a directory, glob or recursively |
| D003.1 | [003](https://github.com/stuliveshere/pyseis/issues/82) | CI | No automated CI runs; all tests are run on demand |
| D003.2 | [003](https://github.com/stuliveshere/pyseis/issues/82) | Deleted corpus manifest and fetch script | Restore both from the last commit and verify they download the test data; goal is one on-demand script that fetches the corpus, checked against manifest checksums |
| D004.1 | [004](https://github.com/stuliveshere/pyseis/issues/83) | Patch the current code before the redesign? | Yes. Each hotfix is its own small GitHub issue, and all are fixed on the current code before any redesign work starts |
| D004.2 | [004](https://github.com/stuliveshere/pyseis/issues/83) | `SEGYExporter` `header_def`/`mapping_path` | Remove them, as their own hotfix (H09). Exporter mappings will come from the `headers.yaml` aliases (001, 007) |
| D004.3 | [004](https://github.com/stuliveshere/pyseis/issues/83) | Aux channel sets in the current SEG-D reader | Include aux by default; flag the behaviour change in the changelog |
| D005.1 | [005](https://github.com/stuliveshere/pyseis/issues/84) | Errors, warnings, provenance and logs | Four separate things (see Summary). Errors: returned result + logs, never provenance, nothing committed. Warnings: result + logs, and saved in the dataset when about the data. Provenance: manifest. Logs: per-run JSON lines linked by run ID. One structured result per operation. Partial-success skips recorded in provenance as warnings |
| D005.2 | [005](https://github.com/stuliveshere/pyseis/issues/84) | Code format | Readable UPPER_SNAKE strings, never renamed once released |
| D005.3 | [005](https://github.com/stuliveshere/pyseis/issues/84) | Exception hierarchy | One base `PyseisError` with families: input, validation, header-not-found, dataset (manifest/commit), export |
| D006.1 | [006](https://github.com/stuliveshere/pyseis/issues/85) | In-memory datasets | Same object as on-disk (same API and manifest structure), backed by memory; writing is the explicit save step. `from_buffer`/`to_buffer` removed; bytes transfer via `pack`/`unpack` |
| D006.2 | [006](https://github.com/stuliveshere/pyseis/issues/85) | Existing single-file `.parquet` datasets | Clean break: no existing Parquet users, so no compatibility code; re-read from original SEG-Y/SEG-D |
| D006.3 | [006](https://github.com/stuliveshere/pyseis/issues/85) | Class name | `SeismicDataset` |
| D006.4 | [006](https://github.com/stuliveshere/pyseis/issues/85) | `gathers()` with no declared order or view | Every dataset always has a native view (written order, one part = one gather); `gathers()` walks it. It asserts no seismic meaning |
| D006.5 | [006](https://github.com/stuliveshere/pyseis/issues/85) | Memory and full loads | Samples only by gather or part; no load-everything option. Whole-dataset load = repartition to one part. Headers can be loaded whole. Per-gather guard, configurable and scaled to machine RAM (~2 GB to ~500 GB) |
| D007.1 | [007](https://github.com/stuliveshere/pyseis/issues/86) | Export order | Export always reads through a view; the chosen view is the write-out order; the native view if none is named; the view used is recorded |
| D007.2 | [007](https://github.com/stuliveshere/pyseis/issues/86) | SEG-Y coordinate scalars | Calculated automatically from the data's precision unless set manually; recorded |
| D007.3 | [007](https://github.com/stuliveshere/pyseis/issues/86) | Canonical columns with no target header | Fixed default header map per format; unmapped columns dropped with a warning listing them; never written into unused bytes implicitly; users can override or modify the map |
| D008.1 | [008](https://github.com/stuliveshere/pyseis/issues/87) | View storage | Inside the dataset folder under `views/`, registered in the manifest |
| D008.2 | [008](https://github.com/stuliveshere/pyseis/issues/87) | Views after a key-changing overlay | No "stale" state: views and declared orders are tied to the version they were built against; a key-changing overlay means they aren't offered in the new version; the old version still has them; the native view always exists |
| D008.3 | [008](https://github.com/stuliveshere/pyseis/issues/87) | Stored sortedness hints | Never stored; `inspect`/`describe` compute suggestions on demand |
| D009.1 | [009](https://github.com/stuliveshere/pyseis/issues/88) | Precedence when overlays touch the same column | Within a branch, the later overlay wins (version order) |
| D009.2 | [009](https://github.com/stuliveshere/pyseis/issues/88) | Named overlay stacks | Git-style branching in the manifest (016): versions form a tree; a branch is a named pointer; samples shared; merging deferred, and conflicts will fail noisily with the user choosing |
| D009.3 | [009](https://github.com/stuliveshere/pyseis/issues/88) | Flattening overlays into base | New base header files (one per part, row-aligned) with overlays applied, as a new version with no overlays; old files kept so earlier versions still work |
| D009.4 | [009](https://github.com/stuliveshere/pyseis/issues/88) | Partial overlays | Allowed; traces not covered keep values from the layer below |
| D010.1 | [010](https://github.com/stuliveshere/pyseis/issues/89) | Pack format | Moved: pack vs archive is settled in the projects issue (018) |
| D010.2 | [010](https://github.com/stuliveshere/pyseis/issues/89) | Re-sort mechanism | Both, by user choice: a view for QC or subsets; a re-sort writing a new dataset for a permanent order. Benchmarking only decides the internal implementation |
| D010.3 | [010](https://github.com/stuliveshere/pyseis/issues/89) | Compaction trigger | Only on request; pyseis hints when it notices many small parts |
| D011.1 | [011](https://github.com/stuliveshere/pyseis/issues/90) | `describe()` output | Fixed, versioned JSON structure, published alongside the metadata contract |
| D011.2 | [011](https://github.com/stuliveshere/pyseis/issues/90) | `inspect` depth | Three levels (light, medium, deep); the user chooses level and file list; runs combinable; results state the level; suggested keys carry matching confidence |
| D011.3 | [011](https://github.com/stuliveshere/pyseis/issues/90) | What tools return | Fixed compact summary per tool, hard size cap enforced by test, unaffected by verbosity; errors and data-changing warnings always included; full detail in the JSON-lines run log, whose detail level verbosity controls; log query command; Python returns the full object |
| D012.1 | [012](https://github.com/stuliveshere/pyseis/issues/91) | CLI framework | Built-in `argparse`; the CLI parses flags and calls the same Python API; thin (mostly `pyseis run flow.yaml` plus look-ups) |
| D012.2 | [012](https://github.com/stuliveshere/pyseis/issues/91) | Exit codes | 0 success, 1 internal bug, 2 bad usage or input, 3 validation failure, 4 partial success; detail in the returned error code |
| D012.3 | [012](https://github.com/stuliveshere/pyseis/issues/91) | Command set | Centred on `pyseis run flow.yaml`; look-ups (inspect, describe, headers, validate, log query, schema browsing, trace display); management (views, versions and branches, archive and pack, cleanup); each lands with its feature |
| D013.1 | [013](https://github.com/stuliveshere/pyseis/issues/92) | Agent context file | `AGENTS.md` (cross-tool standard) plus a one-line `CLAUDE.md` pointing to it |
| D013.2 | [013](https://github.com/stuliveshere/pyseis/issues/92) | Documentation site | Markdown in the repo; no documentation site for now (MkDocs later if needed) |
| D014.1 | [014](https://github.com/stuliveshere/pyseis/issues/93) | Minimum Python | 3.12 |
| D014.2 | [014](https://github.com/stuliveshere/pyseis/issues/93) | Dependencies | Core only: numpy, pandas, pyarrow, pyyaml, jsonschema, Dask. No extras for now; matplotlib and geopandas checked at use time with install hints; extras added when needed |
| D014.3 | [014](https://github.com/stuliveshere/pyseis/issues/93) | Versioning | Semantic versioning from 0.2.0 for the redesign; the dataset format has its own version number |
| D015.1 | [015](https://github.com/stuliveshere/pyseis/issues/94) | Unified model | Every reader produces the same in-memory Arrow dataset; optional steps operate on it; writing is the explicit final step; ingest = read + write |
| D015.2 | [015](https://github.com/stuliveshere/pyseis/issues/94) | Meaning of "in memory" | A stream of gathers or parts, never the whole survey at once |
| D016.1 | [016](https://github.com/stuliveshere/pyseis/issues/95) | Versioning | Every commit creates a version recorded in the manifest; open any version; views and overlays tied to their version |
| D016.2 | [016](https://github.com/stuliveshere/pyseis/issues/95) | Branches | Git-style: versions form a tree, a branch is a named pointer, samples shared |
| D017.1 | [017](https://github.com/stuliveshere/pyseis/issues/96) | Cleanup tools | Garbage collection, prune versions, drop samples (keeping manifest, history, provenance, views, optionally headers) |
| D017.2 | [017](https://github.com/stuliveshere/pyseis/issues/96) | Regenerating dropped samples | Supported from provenance while the parent exists |
| D018.1 | [018](https://github.com/stuliveshere/pyseis/issues/97) | Projects | A folder of datasets plus a project manifest with lineage graph and shared settings; globally unique dataset IDs |
| D018.2 | [018](https://github.com/stuliveshere/pyseis/issues/97) | Pack vs archive | Pack: one version of one dataset as a flat single Parquet file for interchange. Archive: tar of a whole dataset or project with all versions, branches, overlays, views and lineage |
| D018.3 | [018](https://github.com/stuliveshere/pyseis/issues/97) | Transferring a single dataset | Carries parent references; warns and offers to include parents it depends on |
| D019.1 | [019](https://github.com/stuliveshere/pyseis/issues/98) | Main agent interface | Flow files (YAML) as recipe and, via provenance, history; Python scripts remain available |
| D019.2 | [019](https://github.com/stuliveshere/pyseis/issues/98) | Linking modules | Linear stream first, one gather at a time; modules may take other datasets as parameters; full graph later if needed |
| D019.3 | [019](https://github.com/stuliveshere/pyseis/issues/98) | Python fallback | Python modules allowed; their code captured in provenance |
| D019.4 | [019](https://github.com/stuliveshere/pyseis/issues/98) | Executor | Pluggable (serial, process pool, Dask); default Dask local cluster on a single workstation or laptop; clusters deferred (F05) |

### Deferred

| ID | Issue | Decision | Notes |
|---|---|---|---|
| D000.8 | [000](https://github.com/stuliveshere/pyseis/issues/79) | Zarr side: MDIO v1 vs own layout | Deferred. Feature request F01; the Parquet design must not preclude it |
| D001.9 | [001](https://github.com/stuliveshere/pyseis/issues/80) | Reading the CRS from SEG-Y/SEG-D headers | Deferred (F04) |
| D016.3 | [016](https://github.com/stuliveshere/pyseis/issues/95) | Merging branches | Deferred |

