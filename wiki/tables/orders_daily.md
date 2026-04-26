---
type: table
name: orders_daily
status: draft
owner: [[data-platform-team]]
sources: [raw/pipelines/orders_daily.sql]
source_hashes: {raw/pipelines/orders_daily.sql: 319b2b89c80ee01f}
tags: [mart, finance, ops, daily, stable]
last_updated: 2026-04-26
---

# orders_daily

**Daily order rollup mart table.** One row per `(order_day, currency)`. Materialized as `mart.orders_daily` by the dbt model in [[orders_daily_pipeline]]. Powers BI dashboards and the gross-GMV variant in [[gmv|GMV]].

## Grain
One row per `(order_day, currency)` over orders with [[orders__status|status]] in (`paid`, `shipped`, `delivered`). Pending and cancelled orders are excluded.

## Columns
| Column | Type | Description |
| --- | --- | --- |
| [[orders_daily__order_day\|order_day]] | `DATE` | `date_trunc('day', orders.placed_at)`. |
| [[orders_daily__currency\|currency]] | `CHAR(3)` | ISO 4217, copied from [[orders__currency]]. |
| [[orders_daily__orders_paid\|orders_paid]] | `INTEGER` | Count where `status='paid'`. |
| [[orders_daily__orders_shipped\|orders_shipped]] | `INTEGER` | Count where `status='shipped'`. |
| [[orders_daily__orders_delivered\|orders_delivered]] | `INTEGER` | Count where `status='delivered'`. |
| [[orders_daily__orders_total\|orders_total]] | `INTEGER` | Sum of the three above. |
| [[orders_daily__gmv_gross_cents\|gmv_gross_cents]] | `BIGINT` | `SUM(orders.total_cents)` — the gross GMV figure. |

## Upstream
- [[orders_daily_pipeline]] writes this table via dbt.
- Source files: `raw/pipelines/orders_daily.sql`. Indirectly: [[orders]] (via [[stg_orders]]).

## Downstream
- [[payments_reconciliation_dag]]'s `reconcile_payments` task reads this table to compute variance against captured [[payments]].
- BI dashboards read `gmv_gross_cents` directly for the gross GMV column.
- Powers [[gmv|GMV]] (gross variant). The net-cash variant aggregates [[payments]] instead — see the contradiction note on the [[gmv]] page.

## Notes
- **Gross, not net.** `gmv_gross_cents` does not subtract refunds. Finance uses a different number (per `raw/slack/2026-04-20-gmv-definition-debate.md`) — see [[gmv|GMV]].
- `orders_total` is a derived sum, not an independent count — it equals `orders_paid + orders_shipped + orders_delivered` by construction.
