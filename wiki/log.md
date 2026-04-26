# Wiki activity log

Append-only. Newest entry at the top. See [[CLAUDE|operating manual]] for entry format.

---

## 2026-04-26 — Ingest: `orders_daily.sql`, `payments_reconciliation_dag.py`, `2026-04-20-gmv-definition-debate.md`

- **Trigger:** ingest (batch — three related sources at once)
- **Source(s):**
  - `raw/pipelines/orders_daily.sql` (dbt model)
  - `raw/pipelines/payments_reconciliation_dag.py` (Airflow DAG)
  - `raw/slack/2026-04-20-gmv-definition-debate.md` (Slack thread)
- **Pages added:**
  - **Tables (1):** [[orders_daily]] — mart table produced by the dbt model.
  - **Columns (7):** [[orders_daily__order_day]], [[orders_daily__currency]], [[orders_daily__orders_paid]], [[orders_daily__orders_shipped]], [[orders_daily__orders_delivered]], [[orders_daily__orders_total]], [[orders_daily__gmv_gross_cents]].
  - **Pipelines (1, stub):** [[stg_orders]] — referenced by the dbt model via `{{ ref('stg_orders') }}` but staging SQL not yet ingested.
- **Pages updated:**
  - [[orders_daily_pipeline]] — promoted **stub → draft**. Filled in inputs, output mart table, transformation, failure modes from the dbt SQL.
  - [[payments_reconciliation_dag]] — promoted **stub → draft**. Filled in schedule (06:00 UTC daily), SLA (3h), task DAG (`run_orders_daily >> reconcile_payments >> emit_variance`), variance threshold ($5k pages oncall) from the DAG file.
  - [[gmv]] — added `CONTRADICTION:` block citing the Slack thread; named which team owns which definition (Finance: net cash; Growth/BI: gross). Tagged `disputed`.
  - [[orders]] — Downstream link to [[orders_daily]] now resolves as a wiki link (was plain text).
  - [[data-platform-team]] — added [[orders_daily]] to owned tables; added [[stg_orders]] to owned pipelines.
  - [[index]] — counts updated (7 tables / 47 columns / 3 pipelines), new pages added, stubs list reduced to just [[stg_orders]], open questions section gained the GMV labelling decision.
- **Contradictions / open questions:**
  - **NEW** — [[gmv]] now carries a `CONTRADICTION:` over what "GMV" means. Finance treats GMV as net cash (capture-time, refunds subtract). Data Platform/BI ship gross GMV (placement-time, refunds don't subtract). Growth needs gross for the funnel. All three positions documented with sources. Resolution: wiki names both variants; BI dashboard column relabelling deferred (no deadline; owner: BI team).
- **Stubs created:** [[stg_orders]] — drop the staging dbt SQL into `raw/pipelines/` to fill it in.

Notable lineage facts captured:
- `mart.orders_daily.gmv_gross_cents` is the materialized form of the gross-GMV variant; BI reads it directly.
- [[payments_reconciliation_dag]] is the orchestrator for [[orders_daily_pipeline]] — the dbt model has no schedule of its own.
- The Airflow DAG's `reconcile_payments` task is the seam where gross (`orders_daily.gmv_gross_cents`) and net cash (`SUM(payments.amount_cents) WHERE status='captured'`) meet — variance >1% per `(day, currency)` lands on the ops dashboard; total daily variance >$5k pages oncall.

Tooling run after ingest:
- `python tools/check-drift.py --update` — refreshed `source_hashes` on all touched pages.
- `python tools/lint.py` — clean (no errors, no warnings).

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
