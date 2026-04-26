---
type: column
name: orders_daily.orders_total
status: draft
owner: [[data-platform-team]]
sources: [raw/pipelines/orders_daily.sql]
source_hashes: {raw/pipelines/orders_daily.sql: 319b2b89c80ee01f}
tags: [stable]
last_updated: 2026-04-26
---

# orders_daily.orders_total

**Type:** `INTEGER` · **Nullable:** no · **Default:** 0

**Definition.** Total count of [[orders]] in this `(order_day, currency)` bucket — `count(*)` over the same `paid`/`shipped`/`delivered` filter as the per-status columns. Equals [[orders_daily__orders_paid|orders_paid]] + [[orders_daily__orders_shipped|orders_shipped]] + [[orders_daily__orders_delivered|orders_delivered]] by construction.

## Belongs to
[[orders_daily]]

## Lineage
- **Produced by:** [[orders_daily_pipeline]] — `count(*)` after the status filter.
- **Consumed by:** BI dashboards.

## Notes
- Pending and cancelled orders are excluded by the upstream filter — this is not a count of all orders ever placed on that day.
