---
type: column
name: orders_daily.orders_paid
status: draft
owner: [[data-platform-team]]
sources: [raw/pipelines/orders_daily.sql]
source_hashes: {raw/pipelines/orders_daily.sql: 319b2b89c80ee01f}
tags: [stable]
last_updated: 2026-04-26
---

# orders_daily.orders_paid

**Type:** `INTEGER` · **Nullable:** no · **Default:** 0

**Definition.** Count of [[orders]] in this `(order_day, currency)` bucket whose [[orders__status|status]] is `paid`. See [[order-lifecycle|order lifecycle]] for the full state machine.

## Belongs to
[[orders_daily]]

## Lineage
- **Produced by:** [[orders_daily_pipeline]] — `SUM(CASE WHEN status='paid' THEN 1 ELSE 0 END)`.
- **Consumed by:** BI dashboards funnel/conversion charts.

## Notes
- A single order moves through `paid` → `shipped` → `delivered`; on any given day it is counted under whichever status it currently holds, not all three. Re-running the pipeline for a past day reflects the current state of those orders, not their state on that day.
