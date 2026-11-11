# pyseis scope statement

*Agreed in the strategic review of 2026-11-11, after tagging `v0.1.0`. This page sets the direction; the design detail is in the issues indexed in [`issues/README.md`](issues/README.md). Where an issue and this page disagree on scope or priority, this page wins.*

## Who it is for

- **Next 12 months:** Stu Fletcher and the AI agents working for him, on real field data.
- **After that:** the wider geophysics community, once pyseis is relatively stable.

Agents are first-class users. Every operation should be inspectable, repeatable and self-describing, and should refuse to guess.

## What pyseis is

A seismic processing system built on a solid IO and dataset foundation:

1. **IO:** schema-driven readers and writers for field and exchange formats.
2. **Dataset:** a Parquet-based trace store with an explicit metadata contract.
3. **Flows:** a read → flow → write model that moves data through memory in parts, never the whole survey at once.
4. **Processing modules:** defined, well-tested modules that agents and people call from flows. Processing is not left to scripts written fresh each time, although Python scripts stay available.

## The first job

Read field data, optionally edit headers, and write it out in another format, using the read → flow → write model.

- **Starting point:** SEG-D to SEG-Y, and SEG-Y to SEG-D.
- **Why this first:** once data moves through flows in bounded-memory parts, processing modules such as moveout and stack slot into the same structure.

## Not yet

| Item | Position |
|---|---|
| JavaSeis | Deferred until the major refactoring is done. The longer-term need is SEG-D 3.x to JavaSeis, because ProMAX cannot read the newer SEG-D revisions. |
| RSF (Madagascar) | Deferred. |
| Zarr/MDIO hypercubes, MCP server, custom CRS, Dask on clusters, preview tables | Deferred as feature requests F01–F05. |
| Community release work (PyPI, documentation site, contributor process) | Waits until pyseis is stable. |

## Positions on open risks

- **Views** are a convenience for light QC, such as lifting one line out of a volume. They are built as designed (issue 008), then tested. Alternatives are considered only if they prove too slow to use.
- **Table format.** The design builds a minimal manifest over plain Parquet files (D000.7). Existing formats such as Lance and Delta Lake will be reviewed at a point set by the milestones.
- **Licence.** AGPL-3.0 stays for now. The intent is to release openly once there is a viable product, and to earn through consulting, not by restricting the code.

## Still to settle

- **Milestones and the size of 0.2.0.** The build order in the issue index lists phases, but no release boundaries.
- **The processing module library.** Issue 019 defines how modules plug into flows. No issue yet says which modules exist, in what order, or how each is proven correct.
