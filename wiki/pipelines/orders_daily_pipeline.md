---
type: pipeline
name: orders_daily_pipeline
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql, raw/pipelines/orders_daily.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f, raw/pipelines/orders_daily.sql: 319b2b89c80ee01f}
tags: [dbt, scheduled, daily]
last_updated: 2026-04-26
---

# orders_daily_pipeline

**dbt model that aggregates [[orders]] into a daily mart table for BI and finance reporting.** Materialized as `mart.orders_daily` — one row per `(order_day, currency)`. Triggered by [[payments_reconciliation_dag]] at 06:00 UTC daily.

The dbt model file is `models/marts/orders_daily.sql` (source: `raw/pipelines/orders_daily.sql`). Materialization: `table`. Schema: `mart`. Tags: `daily`, `orders`, `core`.

## Inputs
- [[orders]] (via the staging model [[stg_orders]] referenced by `{{ ref('stg_orders') }}`)
- Filter: `status in ('paid', 'shipped', 'delivered')` — pending and cancelled orders are excluded.

## Outputs
- [[orders_daily|mart.orders_daily]] — daily rollup keyed on `(order_day, currency)`.
- Columns produced: [[orders_daily__order_day|order_day]], [[orders_daily__currency|currency]], [[orders_daily__orders_paid|orders_paid]], [[orders_daily__orders_shipped|orders_shipped]], [[orders_daily__orders_delivered|orders_delivered]], [[orders_daily__orders_total|orders_total]], [[orders_daily__gmv_gross_cents|gmv_gross_cents]].

## Transformation
Filters [[orders]] to non-pending, non-cancelled rows (`status in (paid, shipped, delivered)`), buckets by `date_trunc('day', placed_at)::date`, and groups by `(order_day, currency)`. Counts orders per status and sums [[orders__total_cents|total_cents]] into `gmv_gross_cents`.

This is the **gross** GMV variant — refunds are not subtracted because [[orders__total_cents|orders.total_cents]] is frozen at placement (per the source DDL comment). For net-cash GMV see [[gmv|GMV]] and the reconciliation step in [[payments_reconciliation_dag]].

## Failure modes / SLAs
- Failure routes via the parent DAG [[payments_reconciliation_dag]]; the dbt run is the first task there.
- Common failures: schema drift in [[orders]] breaking `stg_orders`; null `placed_at` (data quality issue upstream of the warehouse — should not happen because column is `NOT NULL` per `raw/schemas/sample_ecommerce.sql`).

## Notes
- `stg_orders` is referenced but not yet documented in detail — see [[stg_orders]] stub. Drop the staging model SQL into `raw/pipelines/` to fill it in.
- Powers [[gmv|GMV]] (gross variant) directly via [[orders_daily__gmv_gross_cents]].
