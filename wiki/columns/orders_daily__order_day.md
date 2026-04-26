---
type: column
name: orders_daily.order_day
status: draft
owner: [[data-platform-team]]
sources: [raw/pipelines/orders_daily.sql]
source_hashes: {raw/pipelines/orders_daily.sql: 319b2b89c80ee01f}
tags: [stable]
last_updated: 2026-04-26
---

# orders_daily.order_day

**Type:** `DATE` · **Nullable:** no · **Default:** —

**Definition.** UTC calendar day, computed as `date_trunc('day', orders.placed_at)::date`. Part of the natural key alongside [[orders_daily__currency|currency]].

## Belongs to
[[orders_daily]]

## Lineage
- **Produced by:** [[orders_daily_pipeline]] from [[orders__placed_at|orders.placed_at]].
- **Consumed by:** BI dashboards keyed on day; [[payments_reconciliation_dag]]'s reconcile task keys on this column.

## Notes
- UTC day, not local-tz. Cross-timezone reporting needs a separate transform.
