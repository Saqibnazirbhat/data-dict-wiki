---
type: column
name: orders_daily.currency
status: draft
owner: [[data-platform-team]]
sources: [raw/pipelines/orders_daily.sql]
source_hashes: {raw/pipelines/orders_daily.sql: 319b2b89c80ee01f}
tags: [stable]
last_updated: 2026-04-26
---

# orders_daily.currency

**Type:** `CHAR(3)` · **Nullable:** no · **Default:** —

**Definition.** ISO 4217 currency code, copied from [[orders__currency|orders.currency]]. Part of the natural key alongside [[orders_daily__order_day|order_day]] — totals are not currency-converted, so a multi-currency day produces multiple rows.

## Belongs to
[[orders_daily]]

## Lineage
- **Produced by:** [[orders_daily_pipeline]] from [[orders__currency|orders.currency]].
- **Consumed by:** BI dashboards (one row per day per currency); [[payments_reconciliation_dag]] joins on this column to [[payments__currency|payments.currency]].

## Notes
- No FX conversion. Cross-currency totals require a downstream transform with a rate table.
