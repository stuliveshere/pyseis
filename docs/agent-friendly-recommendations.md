# Making pyseis Agent- and Token-Friendly: Recommendations

*Review of the IO / format-conversion functionality as of commit `6bb199f` (November 2026). Background: [agent-forward-software-research.md](agent-forward-software-research.md).*

> **Status (2026-11-11):** these recommendations have been broken down into design issues in [`issues/`](issues/README.md), all decided in the 2026-11-11 sessions, with a decision register and build order. Where this document and an issue disagree, **the issue wins**. Mapping:
>
> | Section | Now tracked in |
> |---|---|
> | §1 Docs that contradict the code | H11–H13 (hotfixes), 013 (rewrite, tested examples) |
> | §2 Silent defaults | H01–H10 (hotfixes), 001 (contract rules), 000 D000.6 (length/interval policy) |
> | §3 CLI | 012 (thin argparse CLI centred on `pyseis run flow.yaml`) |
> | §4 `describe()` | 011 (versioned `describe`, three-level `inspect`, capped return messages) |
> | §5 Errors | 005 (errors, warnings, provenance and logs) |
> | §6 Bounded memory | 000 (layout), 002 (streaming ingest), 006 (gather-by-gather access), 019 (Dask execution) |
> | §7 Agent context files | 013 |
> | §8 Smaller items | 001 (provenance, naming), 000 (atomic commits), 014 (Python 3.12, dependencies, packaging), 003 (tests on demand) |
> | New since this review | 006 `SeismicDataset`, 007 exporters, 008 views, 009 overlays, 010 compaction/re-sort, 015 read→flow→write, 016 versions and branches, 017 cleanup, 018 projects/pack/archive, 019 flows and execution, F01–F05 |
>
> The priority order below is replaced by the build order in [`issues/README.md`](issues/README.md).

## Summary

The core design already suits agents well:

- footer metadata readable without loading traces;
- human-editable YAML schemas;
- Arrow/Pandas outputs;
- `CorpusScanner`'s status-enum pattern.

The friction for agents comes from:

- **docs that don't match the code**;
- **silent defaults and silently ignored arguments**;
- **no CLI**;
- **unbounded memory use on import**.

### Priority order

1. Fix doc/code mismatches and silent defaults (§1, §2). Small changes, biggest correctness risk.
2. `describe()` plus `pyseis info` / `convert --dry-run` with JSON output (§3, §4).
3. Exception hierarchy and `AGENTS.md` (§5, §7).
4. Streaming import (§6).

---

## 1. Fix docs that contradict the code

Agents write code from the README, so a wrong example produces wrong code.

| Issue | Where | Fix |
|---|---|---|
| Examples use `source_id` / `cdp_id`, but importers produce `shot_number` / `file_number` / `cdp`. `sd.filter(source_id=105)` raises `KeyError`. | `README.md`, `visualization/viewer.py` default `group_by='source_id'` | Use the canonical names everywhere; change the viewer default. |
| `ps.SEGYReader.to_parquet_buffer()` doesn't exist. | `docs/architecture.md` §4 | Remove it or implement it. |
| `SeismicData.filter()` is documented as predicate pushdown but filters a fully loaded table in memory. Real pushdown is only `open(filters=...)`. | `README.md`, `architecture.md` | Correct the docs, or implement real pushdown (§6). |
| Provenance is documented, but no importer writes any. | `architecture.md` §2 | Implement it (§8) or mark it as planned. |

**Guardrail:** turn the README examples into doctests or a `tests/test_docs.py` so drift fails CI.

## 2. Remove silent defaults and silently ignored inputs

These are the most dangerous problems for an agent. A human might notice a wrong 2 ms; an agent will report the result as correct.

- **Sample-rate fallbacks.** 2 ms is assumed in `SeismicData.sample_rate`, `InternalFormatWriter.write`, and `segd/reader.py` when `base_scan_interval == 0`. `SEGYExporter` falls back to 4 ms. → Raise an error, or record an explicit warning in metadata; never fill in silently.
- **Unit guessing.** `SEGYExporter` treats `sample_rate < 1.0` as seconds and anything else as µs. → Store one canonical `sample_interval_us: int`. Metadata currently holds `sample_rate`, `sample_rate_us` and `sample_rate_ms`, three values that can disagree.
- **Unvalidated `custom_mappings`.** Entries with an unknown or misspelled `segy_key` are silently dropped (`segy/fill_plan.py`). → Validate them and suggest the nearest valid keys.
- **Ignored constructor arguments.** `SEGYExporter.__init__` accepts `header_def` and `mapping_path` and ignores them. → Implement them or remove them.
- **Unused `chunk_size`.** Both importers accept it and never use it. → Implement it (§6) or remove it.
- **Warnings via `print()`.** `su/importer.py` ("Endianness ambiguous, defaulting to Little Endian", file-size/stride mismatch) and `su/exporter.py` print instead of warning. → Use `warnings`/`logging`, and also append to `metadata["warnings"]` so the warnings travel with the dataset.
- **Name collision.** `header_mapping.yaml` maps `dt: sample_rate`, which creates a per-trace column with the same name as the global metadata key but in different units (µs vs s). → Rename it, e.g. `trace_dt_us`.

## 3. Add a CLI with JSON output

Today an agent has to write Python just to ask what's in a file. Proposed commands:

```
pyseis info FILE [--json]            # format, revision, manufacturer, ns, dt_us, n_traces, endian, size; no trace reads
pyseis headers FILE [--json]         # columns + dtype + min/max/n_unique/nulls (Parquet stats where possible)
pyseis scan DIR --format segd        # CorpusScanner; JSON lines output
pyseis convert IN OUT [--dry-run]    # format from extension or --from/--to
pyseis validate FILE                 # schema checks, NaNs, dead traces, key monotonicity
pyseis schema list | show segd/rev2.1/sercel
```

Design rules:

- **`--json` on every command**, plus a `--quiet` mode that prints bare values, one per line.
- **Exit codes with meaning**: 0 OK, 2 bad input, 3 schema not detected, 4 partial success.
- **`convert --dry-run`** reports the detected schema variant, the column mapping (source field → output column), estimated output size and peak memory, and any warnings, then exits without writing.
- **Help text with realistic examples.** Agents copy examples more reliably than they read flag descriptions.

An MCP server isn't warranted yet. A good CLI plus `AGENTS.md` gives nearly all the benefit at minimal token cost.

## 4. Compact, structured summaries

- **`SeismicData.describe() -> dict`**, JSON-serialisable:
  - `n_traces`, `n_samples`, `sample_interval_us`, `format`, `revision`;
  - per column: dtype, min, max, n_unique, null count;
  - detected gather keys (columns where traces sort into contiguous runs).

  Rebuild `summary()` on top of it.
- **A footer/stats-only path.** `describe()` should work on a file path using the Parquet footer and row-group statistics alone, without `to_pandas()`. "What shots are in here?" shouldn't need any samples loaded.
- **`__repr__`** on `SeismicData`, so a REPL shows something more useful than `<... object at 0x...>`.

## 5. Errors an agent can act on

- Define a small hierarchy: `PyseisError` → `SchemaDetectionError`, `HeaderNotFoundError`, `FormatMismatchError`, `ValidationError`.
- Each exception carries a stable `code` attribute.
- **Put the fix in the message.** For example, `filter()`'s `KeyError` should list the available columns or the closest matches ("did you mean `shot_number`?"). The viewer already does this; `filter()` doesn't.
- **Report what was inspected.** SEG-D auto-detection failures should say which bytes were read and which variants were tried.
- Extend `CorpusScanner`'s status/`error_note` pattern to SEG-Y and SU.

## 6. Bounded memory for large inputs

`SEGYImporter` and `SEGDImporter` call `read_all_traces()` and `np.vstack` the results, so a directory of SEG-D sits entirely in RAM before anything is written. An agent can't predict when that will exhaust memory, and an OOM kill leaves it nothing to diagnose.

- Make `chunk_size` real: stream into `pq.ParquetWriter` one row group at a time.
- Report the estimated peak memory in `convert --dry-run`.
- Make `SeismicData.filter()` real pushdown via `pq.read_table(filters=...)` when the dataset is backed by a file.

## 7. Agent context files

- **`AGENTS.md`** at the repo root (aim for ≤ 60 lines):
  - canonical column names and units (seconds vs µs);
  - the dataset and footer-metadata contract;
  - which classes are stable public API;
  - known quirks (SEG-D variant detection order, coordinate scalar convention);
  - how to run the tests.
- **A generated schema reference.** Extend `scripts/generate_schemas.py` to emit a compact, greppable table per revision/manufacturer (field, block, offset, length, type, mapped column). Then an agent can find where `receiver_x` comes from in Sercel rev2.1 without walking nested YAML.
- **Standards PDFs.** `docs/standards/*.pdf` are expensive for agents to read. Keep them, but add text extracts of the key tables that pyseis relies on.

## 8. Smaller items

- **Provenance on import**: input file name and sha256, the schema variant chosen, custom mappings applied, pyseis version and timestamp. This makes agent retries reproducible and gives reviewers an audit trail.
- **Safe writes**: `overwrite=True` is the default everywhere. Default to `False`, and write to a temp file then rename it into place, so a crashed retry never leaves a half-written Parquet file.
- **Naming**: `FILENAME` is the only upper-case column; rename it to `input_file`. The `SEGD_Or_SEGYReader` alias in `segy/importer.py` is just `SEGYReader` and misleads readers; remove it.
- **Dependencies**: `dask`, `zarr` and `matplotlib` are required but barely used by the IO path. Move them to extras (`[viz]`, `[dask]`).
- **Packaging**: `pyproject.toml` package-data references `templates/schemas/*.yaml`, which doesn't exist. `segd/*/*.yaml` doesn't cover three-level paths such as `segd/rev2.1/sercel/*.yaml`. Check that a wheel install includes the manufacturer schemas.
- **Tests**: the local pytest cache shows every test file failing on the last recorded run. That may only mean it was run in the wrong environment, but confirm a clean pass before refactoring.

## Appendix: candidate `describe()` output

```json
{
  "format": "SEG-D",
  "revision": "2.1",
  "manufacturer": "sercel",
  "n_traces": 24000,
  "n_samples": 3001,
  "sample_interval_us": 2000,
  "gather_keys": ["file_number"],
  "columns": {
    "file_number":    {"dtype": "int32",   "min": 1001, "max": 1010, "n_unique": 10, "nulls": 0},
    "channel_number": {"dtype": "int32",   "min": 1,    "max": 2400, "n_unique": 2400, "nulls": 0},
    "receiver_x":     {"dtype": "float64", "min": 451200.0, "max": 463180.0, "n_unique": 2400, "nulls": 0}
  },
  "warnings": []
}
```
