---
type: column
name: orders_daily.orders_shipped
status: draft
owner: [[data-platform-team]]
sources: [raw/pipelines/orders_daily.sql]
source_hashes: {raw/pipelines/orders_daily.sql: 319b2b89c80ee01f}
tags: [stable]
last_updated: 2026-04-26
---

# orders_daily.orders_shipped

**Type:** `INTEGER` · **Nullable:** no · **Default:** 0

**Definition.** Count of [[orders]] in this `(order_day, currency)` bucket whose [[orders__status|status]] is `shipped`.

## Belongs to
[[orders_daily]]

## Lineage
- **Produced by:** [[orders_daily_pipeline]] — `SUM(CASE WHEN status='shipped' THEN 1 ELSE 0 END)`.
- **Consumed by:** BI dashboards.

## Notes
- Bucketed by [[orders__placed_at|placed_at]], not [[orders__shipped_at|shipped_at]]. A row in the rollup for day D counts orders *placed* on D that have *now* reached `shipped`.
