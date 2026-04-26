---
type: column
name: orders_daily.gmv_gross_cents
status: draft
owner: [[data-platform-team]]
sources: [raw/pipelines/orders_daily.sql, raw/slack/2026-04-20-gmv-definition-debate.md]
source_hashes: {raw/pipelines/orders_daily.sql: 319b2b89c80ee01f, raw/slack/2026-04-20-gmv-definition-debate.md: d3845126cec6d675}
tags: [finance, stable]
last_updated: 2026-04-26
---

# orders_daily.gmv_gross_cents

**Type:** `BIGINT` · **Nullable:** no · **Default:** 0 · **Unit:** cents (integer)

**Definition.** Gross GMV — `SUM([[orders__total_cents|orders.total_cents]])` over the bucket's filtered orders. **Refunds are not subtracted.** This is the BI/Growth canonical number; Finance uses a different definition (see [[gmv|GMV]]).

## Belongs to
[[orders_daily]]

## Lineage
- **Produced by:** [[orders_daily_pipeline]] — `SUM(total_cents)` after the status filter.
- **Consumed by:** BI dashboard "GMV" column; weekly Growth review (per `raw/slack/2026-04-20-gmv-definition-debate.md`); [[payments_reconciliation_dag]] reconciles against this.

## Notes
- **Frozen at placement.** Inherits the freeze property of [[orders__total_cents|orders.total_cents]] — once an order is placed, this value cannot move regardless of later refunds, partial shipments, or cancellations.
- For net-cash GMV (capture-time, refunds subtracted), see the [[gmv|GMV]] concept page and aggregate [[payments__amount_cents]] WHERE `status='captured'` instead.
