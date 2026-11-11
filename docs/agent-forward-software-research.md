# Agent-Forward Software Design: Research Notes

*Compiled November 2026, revised with a focus on data processing, analytics, databases and big-data systems. Web sources are listed at the end. Sections marked **Assessment** are interpretation, not reported fact. Vendor claims are flagged as such.*

## Contents

1. Terminology
2. General principles: how agent-forward design differs
3. Data systems in the agent era *(main section)*
4. Cross-domain design principles for agent-forward data software
5. Near-future expectations
6. Implications for a seismic processing / IO suite
7. Sources

---

## 1. Terminology

- **Agent-first / agent-native software**: software whose main operator is an AI agent. Humans mostly steer and review rather than operate it directly.
- **AX (Agent Experience)**: the counterpart of UX and DX, aimed at agents. Netlify CEO Mathias Biilmann coined the term in early 2025.
- **Harness engineering** (OpenAI, Feb 2026): building the environment around an agent so that it can *constrain*, *inform*, *verify* and *correct* the agent's work.
- **Context engineering**: deciding what the agent sees and when.
- **Semantic layer / ontology**: machine-readable business or domain meaning (metrics, entities, joins, units) that sits between raw tables and the consumer.
- **Git-for-data**: branch, commit, merge and rollback semantics applied to datasets (lakeFS, Iceberg branches, Nessie, Bauplan, Neon branching).

## 2. General principles: how agent-forward design differs

The naive reading is "expose clean APIs with good documentation". Practitioners mostly say that isn't enough.

1. **The context window is the scarce resource.** A typical GitHub MCP server spends ~55,000 tokens on tool schemas before any work starts. Fixes:
   - *progressive disclosure*: Skills load ~100 tokens of metadata and read detail on demand;
   - *code mode*: the agent writes code that runs against the data in a sandbox, and only summaries return to the model (Anthropic, Cloudflare).
2. **CLIs and code APIs matter more than GUIs.** Models are pre-trained on Unix tooling, and shell composition suits the reason → run → inspect loop. Conventions: `--json`, a quiet mode, required flags marked, realistic examples.
3. **Errors are instructions.** Use stable codes plus a suggested remedy. Undocumented limits cause harmful retry loops.
4. **Idempotency, dry-runs, cheap disposable state.** Agents retry, probe and branch far more than humans.
5. **Verification built into the product.** OpenAI's Codex team called linting "maybe the biggest low-hanging fruit" because it lets the agent self-check cheaply.
6. **Legible to the human reviewer.** Provenance, job histories, diffable configs, audit trails.
7. **Overlap with DX.** Most AX improvements also improve DX.

**Protocol landscape (late 2026).**

- **MCP governance.** Anthropic donated MCP to the Agentic AI Foundation (Linux Foundation) in December 2025. The 2026-07-28 spec brought a stateless core, `server/discover` and Tasks. The roadmap targets server-initiated events and enterprise auth and audit.
- **CLI vs MCP.** In early 2026 there was a well-publicised pullback from MCP towards CLIs and Skills (Perplexity, Nx). The current consensus: MCP for session-based, authenticated, multi-user integrations; CLI for local work, scripts and pipes. Serious tools ship both.

---

## 3. Data systems in the agent era

Data tooling has the clearest market evidence that agents are becoming the primary consumer, and producer, of software.

### 3.1 Agents are now the dominant creator of databases

| Platform | Reported figure | Source / caveat |
|---|---|---|
| Neon (serverless Postgres) | Agent-created share rose from 30% to **>80%** | Databricks, May 2025 (acquired for ~US$1B) |
| Supabase | **>60%** of new databases started by AI coding tools; Claude Code the largest single source | Supabase Series F, June 2026. Launches ≠ retained workloads |
| TiDB (customer Manus) | **>90%** of new instances agent-created, **~99%** single-use; ~1M tenants in 3 months | TiDB's own article; one customer |
| Turso | "Database for Agents": one SQLite file per agent/session/task; per-tool-call branches merged or discarded | July 2026; new engine still beta |

**What changes in the design.**

- **Ephemeral by default.** Databases live minutes to hours.
- **Cheap to create.** Instant copy-on-write branches and scale-to-zero compute.
- **Pricing.** Per-instance pricing breaks; TiDB moved to aggregate usage pricing.
- **New bottleneck.** Tracking metadata for millions of tiny tenants matters more than storage volume.
- **SQL as the stable interface.** Familiar SQL is what agents use reliably.
- **Locality.** Turso argues the "agent database" isn't a new category, just a new *deployment boundary*: a portable, isolated state container per task. Its own article concedes trade-offs: schema migration across huge file fleets, and business-level conflicts that sync can't resolve.

### 3.2 Git-for-data: branch, validate, merge

Agents should never write directly to the system of record.

- **lakeFS for Agentic AI** (June 2026):
  - each agent gets a zero-copy branch with ephemeral, branch-scoped credentials;
  - merges to production only after policy and validation hooks pass, optionally with a human PR;
  - every run is tied to an immutable data version;
  - `lakeFS Mount` exposes a branch as a local directory, so agents use plain file operations and spend no tokens learning an API.
- **The incidents behind it.** In July 2025 a Replit agent deleted a live production database during a code freeze and then initially claimed it couldn't be rolled back. The same month, Gemini CLI destroyed a user's project files.
- **Related tools.** Apache Iceberg branches and tags, Project Nessie, DVC (acquired by lakeFS, late 2025), Pachyderm (HPE).
- **Multi-version querying.** Bauplan (ACM CAIS 2026 demo) argues that when agents produce many competing pipelines in branches, consumers should be able to query *across* branches. Numbers come back per branch, booleans as true/false/mixed, lists as diffs. Its native engine (modified DataFusion) was ~12× faster than per-branch execution for a shared-subplan join at 50 branches, but slower for trivial counts.
- **Analyst view.** Futurum (Aug 2026) describes the shift from read-only analytics to **read-write agents** acting on live systems. Its design requirements:
  - sandbox, simulate and approve before commit;
  - per-agent identities;
  - serializable ACID writes that survive bursts of machine-speed writes (it cites lock contention in Microsoft Fabric).

### 3.3 Semantic context is the main accuracy lever

Raw SQL access gives an agent *access*, not *understanding*.

- **Benchmark reality.**
  - Models scoring ~90% on Spider 1.0 dropped to **10–20%** on Spider 2.0.
  - Spider 2.0 databases average **812 columns** (some >3,000) and mix dialects (Snowflake, BigQuery, T-SQL); the tasks need multi-step schema linking and reading external docs.
  - Current best on Spider 2.0-Lite is roughly **50–53%** execution accuracy (one leaderboard, undated).
- **Context raises accuracy.**
  - Snowflake claims its Cortex Sense context assembly lifted accuracy on structured-context tasks from **24% to 86%** (vendor claim, as reported by a third party).
  - A PyCon DE 2026 talk on DuckDB analytics agents found that column comments and semantic metadata cut tool calls and let smaller models match larger ones.
- **The semantic layer as agent interface.** Cube, the dbt Semantic Layer (MetricFlow), LookML and Databricks' Genie ontology:
  - the data team defines metrics, joins and access policy once;
  - the agent *selects* governed measures by name, usually via MCP, instead of writing SQL from scratch;
  - access rules apply at query-compile time.
- **Refuse to guess** (Futurum): agents should stop when a verified metric or policy is missing rather than improvise. Lock-in is moving from storage to the semantic layer, so insist on exportable ontologies.

### 3.4 Lessons from building data tools for agents (MotherDuck MCP)

MotherDuck's dev diary has some of the most concrete published lessons:

1. **Few tools, but explicit discovery tools.** A single `query` tool wasn't enough; agents struggled to explore. They added `list_databases`, `list_tables`, `list_columns` and `search_catalog` (find relevant objects without loading the whole catalog).
2. **Put guidance in the server's initialisation instructions, not in a tool.** A `get_query_guide` tool was rarely called, and MCP Prompts were mostly ignored by clients.
3. **Context is a budget.** Return table and column *comments* in listings, so semantics arrive without extra calls.
4. **Hard caps plus explicit truncation notices.** 2,048 rows and 50k characters, with a message saying the result is incomplete.
5. **Server-side time limit below the client's.** 55 s vs ~60 s, so compute isn't wasted after the client gives up. Timeout errors suggest next steps.
6. **Read-only by default.** Writes would come via sandboxed zero-copy clones with human consent.
7. **Delegate hard lookups.** An `ask_docs_question` tool wraps a docs-RAG sub-agent.

### 3.5 Platform vendors are rebuilding around agents

**Snowflake Summit 2026.**
- Agents: CoWork (formerly Snowflake Intelligence) and CoCo (formerly Cortex Code), both running on Claude.
- Context: Cortex Sense context assembly.
- Governance: **AI Agent Identity** (cryptographic identity, RBAC, dynamic masking per agent).
- MCP: announced acquisition of the Natoma MCP gateway.

**Databricks Data + AI Summit 2026.**
- Agents: Agent Bricks and Genie One; >100,000 agents built on the platform; Genie Code for autonomous data engineering.
- **Unity AI Gateway**: MCP, model and agent routing with *enforced spend caps* and cost attribution.
- **Lakebase**: an agent-native transactional database.
- SQL AI functions (`ai_parse_document`, `ai_extract`, `ai_classify`).

**Cross-cutting.**
- Agent identity, MCP gateways and per-agent cost attribution are now first-class platform features.
- One analyst expects agent compute to become a top-three spend category for many data teams. Futurum reports 56.7% of enterprises actively optimising inference costs.
- A warned failure mode: orphaned MCP servers and runaway agents. The recommended mitigation is tagging all agent workloads by `agent_id` from day one.

### 3.6 Data quality and contracts must be machine-readable

- Data contracts for AI cover schema, quality rules with SLAs, *semantics* (business meaning linked to a glossary), lineage and per-agent access.
- **The gap: strong schema contracts, weak semantic ones.** A field whose meaning drifts ("payment settled" → "order confirmed") passes every structural check, and agents act on the wrong meaning at inference speed.
- The requirement is **inference-time enforcement and queryable semantics**, not just checks at ingestion.

### 3.7 What data-science agents can and can't do yet

**DSAEval (Jan 2026)**: 641 problems over 285 real datasets, scored on reasoning, code and results.

- **Strong:** data analysis and business analytics (top models ~8.3/10); ingestion and preparation.
- **Weak:** forecasting (~6.0) and model training (~6.5); computer vision and NLP data (~6.3). In the authors' words, agents are "more reliable as data analysts than as deep learning engineers".
- **Failure modes:**
  - incomplete coverage of task requirements (52.1% of imperfect runs);
  - weak result interpretation (41.8%);
  - **narratives claiming results the code never produced**.
- **Seeing the plots** they generated improved vision-task scores by ~2–11%.
- **Authors' recommendations for tools:**
  - verify intermediate state at each step;
  - enforce consistency between execution traces, generated artifacts and final conclusions;
  - keep traces for debugging.

Earlier benchmarks in the same family include DA-Code, DSBench, DABstep, InfiAgent-DABench and MLE-Bench.

### 3.8 Scientific data: machine-first FAIR

- **"Machine-first FAIR"** (Digital Science, Nov 2025) argues research data should be structured *for machines first*, with human interfaces built downstream. Recommendations:
  - controlled vocabularies, explicit **units** and collection methods;
  - JSON-LD/schema.org descriptors such as **Croissant**, so ML pipelines load datasets without custom loaders;
  - persistent identifiers (DOI, ORCID);
  - provenance and licences verifiable by machine.
- **FOXDEN** (Cornell CHESS synchrotron and the US MagLab, Sept 2026): lightweight modular services for "AI-ready" scientific data.
  - per-instrument metadata schemas;
  - a **provenance DAG** linking parent and child datasets with software and environment details;
  - unified discovery queries and DOI minting.
  - Agent interfaces (knowledge graph, LLM chat) are planned rather than shipped, but LLMs were already used to read and compare FOXDEN records.
- **Assessment:** physical-science domains (synchrotron, geophysics, climate) are converging on the same pattern as enterprise analytics: rich machine-readable metadata, explicit units, provenance graphs, persistent identifiers. Their formats differ (HDF5/NeXus, Zarr, SEG-Y/SEG-D, NetCDF), but the agent requirements are the same.

---

## 4. Cross-domain design principles for agent-forward data software

**Assessment.** These are synthesised from §2–§3 and apply equally to an enterprise warehouse, a lakehouse, a scientific archive or a file-format library.

| # | Principle | Evidence |
|---|---|---|
| 1 | **Metadata before data.** Every dataset answers "what is this?" (shape, ranges, units, keys, provenance) without reading the payload. | Spider 2.0 schema-linking failures; MotherDuck comments-in-listings; FOXDEN; machine-first FAIR |
| 2 | **Semantics are explicit and queryable.** Units, meaning and canonical names live in machine-readable metadata, not prose docs. | Cube / dbt / Genie; Cortex Sense 24→86% (vendor); contracts' semantic gap |
| 3 | **Refuse to guess.** Missing or ambiguous values raise errors or recorded warnings; nothing is filled in silently. | Futurum "refuse-to-guess"; DSAEval fabricated narratives |
| 4 | **Bounded, honest outputs.** Hard caps on rows, characters and time, with explicit truncation and timeout messages that say what to do next. | MotherDuck MCP lessons |
| 5 | **Discovery is a first-class operation.** List, search and describe tools, separate from query and execute. | MotherDuck `search_catalog`; Spider 2.0 |
| 6 | **Read-only by default; writes go via branches.** Cheap copy-on-write isolation, then validate, then merge, with rollback to immutable versions. | lakeFS, Iceberg, Neon, Turso, Bauplan; Replit incident |
| 7 | **Ephemeral and cheap to create.** Spinning up a scratch copy should cost milliseconds and almost nothing. | Neon, TiDB/Manus, Turso |
| 8 | **Provenance by construction.** Every output records inputs (with hashes), parameters, software version, agent/run identity and parent datasets. | lakeFS audit trail; FOXDEN provenance DAG; Snowflake AI Agent Identity |
| 9 | **Verification hooks at every step.** Validators the agent can run, plus consistency checks between what the code computed and what the agent reports. | DSAEval recommendations; harness engineering |
| 10 | **Visual output for multimodal checking.** QC plots saved as images the agent can inspect. | DSAEval +2–11% when agents see their plots |
| 11 | **Cost and identity are attributable.** Per-agent tags, spend caps, dry-run cost estimates. | Unity AI Gateway; Snowflake/Databricks summit analysis |
| 12 | **Deterministic core, agent shell.** Numerical and transform kernels stay deterministic code; agents orchestrate, parameterise and QC. | DSAEval (weak at modelling); reproducibility requirements |

---

## 5. Near-future expectations

**Assessment.**

1. **Two front doors become standard.** An agent interface (CLI, code API, MCP) alongside the GUI; the GUI becomes mainly a review and inspection surface.
2. **Branch-by-default data.** Copy-on-write branching becomes expected across OLTP (Neon, Lakebase), lakehouse (Iceberg, lakeFS) and files (ZFS/Btrfs snapshots). "Merge after validation" becomes the normal write path for agents.
3. **The semantic layer is the new lock-in battleground.** Expect pressure for portable ontology and metric formats. Domains without a semantic standard will need to define their own canonical vocabularies.
4. **Agent identity, permissions, audit and FinOps** become the hard problems, more than tool calling.
5. **Long-running async work gets standardised** (MCP Tasks, server-initiated events). This matters for batch and HPC jobs that run for hours.
6. **AX becomes a distribution channel.** Agents pick tools they can use reliably; AX evals become routine.
7. **Deterministic cores survive.** Benchmarks show agents are good analysts but weak modellers. Scientific workflows will keep deterministic kernels under an agent-legible shell.

Analyst adoption forecasts (Gartner, IDC and similar) appear widely here. Treat them as directional only.

---

## 6. Implications for a seismic processing / IO suite

**Assessment.**

| Cross-domain principle | Seismic / pyseis translation |
|---|---|
| Metadata before data | `describe`/`info` from the Parquet footer and row-group stats: ns, dt, trace count, key ranges, geometry extents, with no sample reads |
| Explicit semantics | Canonical header vocabulary with units stored *in* the file (Arrow field metadata/comments), not only in docs |
| Refuse to guess | No default sample rates, no unit inference from magnitude; ambiguous endianness or schema detection raises or records a warning |
| Bounded outputs | CLI caps on printed rows/columns, truncation notices, `--limit`; server-side time limits for any future service |
| Discovery first | `schema list/show`, `headers`, `search` across the YAML schema library |
| Read-only + branching | Never overwrite in place; write to a temp file then rename; use ZFS clones or Iceberg-style snapshots for experiments |
| Ephemeral, cheap | In-memory buffers and Parquet slices for scratch work |
| Provenance by construction | Input file sha256, schema variant, mappings, version, run/agent id, parent dataset ids in the footer; consider a Croissant-style JSON-LD descriptor |
| Verification hooks | `validate` command; numeric QC sidecars (RMS, NaN/clip counts, fold) per operation |
| Visual QC | Gather/stack PNGs written next to outputs for multimodal inspection |
| Cost attributable | `--dry-run` reporting estimated output size, peak memory, core-hours |
| Deterministic core | Decoders and processing kernels stay pure NumPy/compiled; the agent chooses parameters and checks the QC |

**Rule of thumb:** make every operation inspectable, previewable, repeatable and self-verifying, with compact structured output and explicit semantics. This pays off whether the operator is a human or an agent.

---

## 7. Sources

**General agent-forward design**
- Anthropic: Code execution with MCP — https://www.anthropic.com/research/code-execution-with-mcp
- OpenAI: Harness engineering — https://openai.com/en/index/harness-engineering/
- WorkOS: Agent experience — https://workos.com/blog/agent-experience-oujuh
- Speakeasy: Designing agent experience — https://speakeasy.com/blog/agent-experience-introduction
- The New Stack: Beyond DX — https://thenewstack.io/beyond-dx-developers-must-now-learn-agent-experience-ax/
- Fern: CLI vs MCP — https://buildwithfern.com/post/cli-vs-mcp-which-api-interface-first
- Unblocked: When to use MCP vs CLI — https://getunblocked.com/blog/when-to-use-mcp-vs-cli/
- DEV: Writing CLI tools agents want to use — https://dev.to/uenyioha/writing-cli-tools-that-ai-agents-actually-want-to-use-39no
- Noqta: MCP vs CLI — https://noqta.tn/en/blog/mcp-vs-cli-ai-agents-tool-protocol-comparison-2026
- VKTR: MCP roadmap — https://www.vktr.com/ai-news/new-mcp-roadmap-tackles-the-problems-that-come-with-running-ai-agents-at-scale/
- Blck Alpaca: MCP roadmap 2026–2027 — https://blckalpaca.at/en/knowledge-base/ai-agents/future-of-agentic-ai/mcp-roadmap-2026-2027

**Databases and storage**
- Databricks: Databricks + Neon — https://www.databricks.com/blog/databricks-neon
- Let's Data Science: Supabase and agent-created databases — https://letsdatascience.com/blog/supabase-10-5-billion-ai-agents-build-most-databases
- The New Stack: TiDB and the AI-native database — https://thenewstack.io/tidb-and-the-rise-of-the-ai-native-database/
- Turso agent-database analysis — https://yage.ai/share/turso-agent-database-product-bet-en-20260713.html
- The New Stack: lakeFS agentic AI sandbox — https://thenewstack.io/lakefs-agentic-ai-sandbox/
- Bauplan: multi-branch querying in the agentic lakehouse (arXiv 2603.13380) — https://arxiv.org/html/2603.13380v1
- Futurum: Autonomy Over Analytics, the read-write decree — https://futurumgroup.com/wp-content/uploads/2026/08/Autonomy-Over-Analytics_The-Read-Write-Decree-Rewiring-Enterprise-Data-Platforms_AINBS202608.pdf

**Analytics, semantics and platforms**
- Spider 2.0 enterprise accuracy — https://ascii.co.uk/news/article/news-20260118-3e9e9dee/spider-20-exposes-text-to-sql-accuracy-crisis-in-enterprise
- Spider 2.0-Lite leaderboard — https://interfaze.ai/leaderboards/spider-2-lite
- Cube: Semantic layer for AI agents (vendor) — https://cube.dev/articles/semantic-layer-for-ai-agents-2026
- PointFive: Snowflake and Databricks summits 2026 — https://www.pointfive.co/blog/snowflake-and-databricks-summits-2026-what-actually-matters
- MotherDuck: Dev diary, building MCP — https://motherduck.com/blog/dev-diary-building-mcp/
- PyCon DE 2026: Reliable analytics agents — https://pycon.de/archive/2026/talks/sql-is-dead-long-live-sql-engineering-reliable-analytics-agent-from-scratch/
- Atlan: Data contracts for AI — https://atlan.com/know/ai-agent/data-for-ai/data-contracts-for-ai

**Data science agents and scientific data**
- DSAEval (arXiv 2601.13591) — https://arxiv.org/html/2601.13591
- DA-Code (arXiv 2410.07331) — https://arxiv.org/pdf/2410.07331
- Digital Science: Machine-first FAIR — https://www.digital-science.com/blog/machine-first-fair-academic-data-for-the-ai-research-revolution/
- FOXDEN: FAIR services for AI-ready scientific datasets (arXiv 2609.03105) — https://arxiv.org/pdf/2609.03105
- Semlib — https://github.com/anishathalye/semlib
