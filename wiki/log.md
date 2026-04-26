# Wiki activity log

Append-only. Newest entry at the top. See [[CLAUDE|operating manual]] for entry format.

---

## 2026-04-26 — Ingest: `sample_ecommerce.sql`

- **Trigger:** ingest
- **Source(s):** `raw/schemas/sample_ecommerce.sql`
- **Pages added:**
  - **Tables (6):** [[users]], [[categories]], [[products]], [[orders]], [[order_items]], [[payments]]
  - **Columns (40):** all columns across the 6 tables — see [[index]] for the full list.
  - **Concepts (3):** [[gmv|GMV]], [[order-lifecycle|order lifecycle]], [[revenue-recognition|revenue recognition]]
  - **Pipelines (2, stub):** [[orders_daily_pipeline]], [[payments_reconciliation_dag]]
  - **Owners (2):** [[data-platform-team|Data Platform team]], [[growth-team|Growth team]]
- **Pages updated:** [[index]] (full inventory)
- **Contradictions / open questions:**
  - [[revenue-recognition]] — exact `shipped` vs `delivered` recognition trigger needs Finance sign-off; BI currently uses `shipped`. Tagged `needs-info`.
- **Stubs created:** [[orders_daily_pipeline]], [[payments_reconciliation_dag]] — both reference the schema header but the pipeline definitions themselves have not been ingested. Drop the dbt model and DAG file into `raw/pipelines/` to fill them in.

Notable lineage facts captured:
- [[orders__total_cents]] is **frozen at placement** — refunds do not decrement it. Net cash uses [[payments__amount_cents]] (signed) WHERE [[payments__status]] = `'captured'`.
- [[order_items__unit_price_cents]] is a price snapshot — never join to current [[products__price_cents]] for past orders.
- Co-ownership: [[users]] product surface is owned by [[growth-team|Growth]]; pipeline is owned by [[data-platform-team|Data Platform]].

---

## 2026-04-26 — Wiki initialized

- **Trigger:** bootstrap
- **Source(s):** none
- **Pages added:** [[index]], [[log]]
- **Pages updated:** —
- **Contradictions / open questions:** —
- **Stubs created:** —

Set up `CLAUDE.md` with workflow definitions (ingest, query, lint), page templates for tables/columns/pipelines/concepts/owners, naming conventions, and tag vocabulary. Empty wiki ready for first ingest.
