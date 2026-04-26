---
type: column
name: orders_daily.orders_delivered
status: draft
owner: [[data-platform-team]]
sources: [raw/pipelines/orders_daily.sql]
source_hashes: {raw/pipelines/orders_daily.sql: 319b2b89c80ee01f}
tags: [stable]
last_updated: 2026-04-26
---

# orders_daily.orders_delivered

**Type:** `INTEGER` · **Nullable:** no · **Default:** 0

**Definition.** Count of [[orders]] in this `(order_day, currency)` bucket whose [[orders__status|status]] is `delivered`.

## Belongs to
[[orders_daily]]

## Lineage
- **Produced by:** [[orders_daily_pipeline]] — `SUM(CASE WHEN status='delivered' THEN 1 ELSE 0 END)`.
- **Consumed by:** BI dashboards; [[revenue-recognition|revenue recognition]] discussion uses this as one option for the recognition trigger.

## Notes
- Bucketed by [[orders__placed_at|placed_at]], not [[orders__delivered_at|delivered_at]]. The count reflects current state of orders placed on that day.
