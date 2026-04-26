# Data Dictionary & Lineage Wiki — Operating Manual

This file is the schema for the wiki. Read it fully before doing any ingest, query, or lint work.

## Purpose

A persistent, compounding knowledge base that documents every table, column, pipeline, owner, and business concept across the data stack. Sources flow in (SQL schemas, dbt models, Airflow DAGs, Slack threads). The wiki is the canonical, human-readable model of the data world.

## Architecture (3 layers)

1. **`raw/`** — immutable source files. **Read only.** Never edit, rename, or delete files in here.
   - `raw/schemas/` — DDL files, dbt model SQL, schema dumps
   - `raw/pipelines/` — Airflow DAGs, dbt project files, orchestration configs
   - `raw/slack/` — exported Slack threads, decision records, tribal knowledge
2. **`wiki/`** — generated, structured markdown. **You own this entirely.** Add, edit, refactor freely.
3. **`CLAUDE.md`** (this file) — the schema. Update it only when conventions change, and log the change.

## Wiki layout

```
wiki/
├── index.md              # entry point, lists everything
├── log.md                # append-only changelog of ingest/lint/refactor activity
├── tables/               # one page per physical table
├── columns/              # one page per column ({table}__{column}.md)
├── pipelines/            # one page per pipeline / DAG / dbt model
├── concepts/             # business concepts (GMV, churn, order lifecycle, ...)
└── owners/               # teams or individuals responsible for data assets
```

## File naming

| Type     | Filename                       | Wiki link                     |
| -------- | ------------------------------ | ----------------------------- |
| table    | `tables/{table}.md`            | `[[{table}]]`                 |
| column   | `columns/{table}__{column}.md` | `[[{table}__{column}]]`       |
| pipeline | `pipelines/{pipeline}.md`      | `[[{pipeline}]]`              |
| concept  | `concepts/{kebab-slug}.md`     | `[[{kebab-slug}\|Display]]`   |
| owner    | `owners/{kebab-slug}.md`       | `[[{kebab-slug}\|Team Name]]` |

Rules:
- All filenames lowercase, snake_case for SQL identifiers, kebab-case for prose slugs.
- Filenames must be unique vault-wide (Obsidian resolves links by basename). The `{table}__{column}` pattern guarantees no collision between table pages and column pages.
- When a name would collide (e.g. a concept named "orders"), suffix the concept: `concepts/orders-concept.md`.

## Cross-linking — Obsidian `[[wiki-link]]` format

- Always link the **first** mention of any entity on a page, and any mention that adds new context.
- Use display aliases for readability: `[[order-lifecycle|order lifecycle]]`.
- Backlinks come for free in Obsidian — do not maintain manual "referenced by" sections.
- If you mention a table/column/pipeline/concept/owner that does not yet have a page, **create a stub** (frontmatter + `status: stub` + a one-line description) so the link is not red. Stubs are tracked in `index.md` under "Stubs awaiting fill".

## Frontmatter (every wiki page)

```yaml
---
type: table | column | pipeline | concept | owner
name: {human-readable name}
status: stub | draft | reviewed
owner: [[owner-slug]]            # omit for owner pages themselves
sources: [raw/schemas/foo.sql, raw/slack/2026-03-12-thread.md]
tags: [pii, finance, deprecated, ...]
last_updated: YYYY-MM-DD
---
```

`status` semantics:
- `stub` — placeholder; only frontmatter + one-line description.
- `draft` — populated from at least one source, but unverified or incomplete.
- `reviewed` — cross-checked against ≥2 sources or explicitly confirmed by an owner in `raw/slack/`.

## Page templates

### Table — `wiki/tables/{table}.md`

```markdown
---
type: table
name: {table}
status: draft
owner: [[owner-slug]]
sources: [...]
tags: [...]
last_updated: YYYY-MM-DD
---

# {table}

**One-line purpose.** What this table represents in the business.

## Grain
One row per {entity / event}. State the natural key.

## Columns
| Column | Type | Description |
| --- | --- | --- |
| [[{table}__id\|id]] | bigint | ... |
| [[{table}__user_id\|user_id]] | bigint → [[users]] | ... |

## Upstream
- [[some-pipeline]] writes this table.
- Source files: `raw/schemas/foo.sql`.

## Downstream
- [[orders_daily_pipeline]] reads from this table.
- Powers [[gmv|GMV]] and [[order-lifecycle|order lifecycle]] reporting.

## Notes
- Gotchas, deprecations, known issues. Cite sources inline: "(per `raw/slack/...`)".
```

### Column — `wiki/columns/{table}__{column}.md`

```markdown
---
type: column
name: {table}.{column}
status: draft
owner: [[owner-slug]]
sources: [...]
tags: [pii, ...]
last_updated: YYYY-MM-DD
---

# {table}.{column}

**Type:** `{sql_type}` · **Nullable:** yes/no · **Default:** ...

**Definition.** Plain-English meaning.

## Belongs to
[[{table}]]

## Lineage
- **Produced by:** [[some-pipeline]] / source DDL.
- **References:** `[[other_table]].[[other_table__id\|id]]` (FK).
- **Consumed by:** [[downstream-pipeline]], [[some-concept]].

## Allowed values / domain
Enum values, ranges, business rules.

## Notes
```

### Pipeline — `wiki/pipelines/{pipeline}.md`

```markdown
---
type: pipeline
name: {pipeline}
status: draft
owner: [[owner-slug]]
sources: [...]
tags: [airflow, dbt, scheduled, ...]
last_updated: YYYY-MM-DD
---

# {pipeline}

**One-line purpose.** Schedule: `{cron / trigger}`.

## Inputs
- [[users]], [[orders]]

## Outputs
- [[orders_daily]]

## Transformation
Brief prose summary of what the pipeline does. Reference SQL files with backticks.

## Failure modes / SLAs
```

### Concept — `wiki/concepts/{slug}.md`

```markdown
---
type: concept
name: {Display Name}
status: draft
owner: [[owner-slug]]
sources: [...]
tags: [metric, lifecycle, ...]
last_updated: YYYY-MM-DD
---

# {Display Name}

**One-paragraph definition.** Why this matters in the business.

## Computed from
- [[orders]].[[orders__total_cents|total_cents]]
- [[payments]].[[payments__status|status]] = 'captured'

## Related concepts
[[revenue-recognition]], [[gmv]]

## Open questions / contradictions
- (date) Source A says X, source B says Y. Resolved/unresolved.
```

### Owner — `wiki/owners/{slug}.md`

```markdown
---
type: owner
name: {Team or Person Name}
status: draft
sources: [...]
tags: [team, individual]
last_updated: YYYY-MM-DD
---

# {Team Name}

**Charter.** What this team is responsible for.

## Owns
- Tables: [[users]], [[orders]]
- Pipelines: [[orders_daily_pipeline]]
- Concepts: [[order-lifecycle|order lifecycle]]

## Contact
Slack: `#data-platform`. Oncall: ...
```

## Workflows

### Ingest — adding a new source

Trigger: user drops a file into `raw/...` and asks you to ingest it (or names the file).

Steps:
1. **Read the source fully** before writing anything.
2. **Inventory** — list every entity it mentions: tables, columns, pipelines, owners, concepts.
3. For each entity:
   - If a wiki page exists → **merge** new info. Preserve existing content unless directly contradicted. When contradicted, keep both with a dated note in `## Notes` and flag in `log.md`.
   - If no page exists → **create** from the relevant template above.
   - For every entity *referenced but not the focus*, create a `status: stub` page so links resolve.
4. **Update `index.md`** — add new pages to the correct section, alphabetized.
5. **Append to `log.md`** — one entry per ingest run with date, source, summary of pages added/updated, and any contradictions flagged.
6. **Bump `last_updated`** on every page touched.

Hard rules:
- Never invent column types, owners, or business definitions. If unknown, write `_unknown_` and tag the page `needs-info`.
- Cite sources inline whenever you make a non-obvious claim: "(per `raw/slack/2026-03-12-thread.md`)".
- One ingest = one `log.md` entry, even if many pages changed.

### Query — answering questions from the wiki

Trigger: user asks a data-dictionary question (e.g. "what does `orders.status` mean?", "who owns payments?", "what feeds GMV?").

Steps:
1. Start at `wiki/index.md` to orient.
2. Read the most specific page first (column → table → concept → pipeline → owner, in that order of specificity).
3. Follow `[[wiki-links]]` only as needed; do not exhaustively traverse.
4. Quote the wiki directly when answering. If the wiki is silent or stubbed, say so explicitly and offer to ingest a source that would fill the gap.
5. Do **not** read `raw/` to answer queries unless the wiki is missing the info — the wiki is the cache.

### Lint — periodic wiki health check

Trigger: user asks for a lint, or you notice drift during ingest.

Checks:
1. **Broken links** — any `[[link]]` whose target file does not exist. Fix by creating a stub or correcting the link.
2. **Orphan pages** — pages with zero inbound links (Obsidian backlinks). Either link them from a relevant page or move to `concepts/` if they are standalone.
3. **Stub debt** — count pages with `status: stub` that are older than 7 days. List them in `index.md` under "Stubs awaiting fill".
4. **Stale pages** — `last_updated` older than 90 days where the source file has changed since. Re-ingest.
5. **Unresolved contradictions** — search `## Notes` sections for the marker `CONTRADICTION:` and surface them.
6. **Missing frontmatter fields** — every page must have `type`, `name`, `status`, `last_updated`.

Output a lint report (do not auto-fix structural issues without user confirmation), then append a `log.md` entry summarizing what was found and what was fixed.

## `index.md` rules

`index.md` is the table of contents. Structure:
1. Header + last-updated date.
2. Counts (tables / columns / pipelines / concepts / owners).
3. Sections per type, alphabetized, one bullet per page with a one-line description pulled from the page's opening line.
4. "Stubs awaiting fill" section listing all `status: stub` pages.
5. "Recently updated" section — top 10 by `last_updated`.

Update `index.md` on every ingest and lint run. Do not let it go stale.

## `log.md` rules

Append-only. Newest entry at the **top**. Entry format:

```markdown
## YYYY-MM-DD — {short title}

- **Trigger:** ingest / lint / refactor
- **Source(s):** `raw/path/to/file`
- **Pages added:** [[a]], [[b]]
- **Pages updated:** [[c]] (added column descriptions), [[d]] (corrected owner)
- **Contradictions / open questions:** ...
- **Stubs created:** [[e]], [[f]]
```

Never rewrite history in `log.md`. If a prior entry was wrong, write a new entry that corrects it.

## Tags — controlled vocabulary

Use these tags consistently (extend only with good reason):
- **Sensitivity:** `pii`, `pci`, `phi`, `internal`
- **Domain:** `finance`, `growth`, `product`, `ops`, `marketing`
- **Lifecycle:** `deprecated`, `experimental`, `stable`
- **Quality:** `needs-info`, `needs-owner`, `disputed`

## Contradictions

When two sources disagree:
1. Keep both claims on the page, each with its source citation and date.
2. Mark with `CONTRADICTION:` prefix in `## Notes`.
3. Set page `status: draft` (never `reviewed` while a contradiction is open).
4. Log it in `log.md`.
5. Resolve only when the user or a new source adjudicates — then write a dated resolution note (do not delete the history).
