---
type: column
name: orders.total_cents
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [finance, stable]
last_updated: 2026-04-26
---

# orders.total_cents

**Type:** `BIGINT` · **Nullable:** no · **CHECK:** `>= 0`

**Definition.** Total amount of the order at placement time, in minor units of [[orders__currency|currency]]. **Frozen** — does not change on refund.

## Belongs to
[[orders]]

## Lineage
- **Produced by:** checkout — sum of `quantity * unit_price_cents` across [[order_items]].
- **Consumed by:** [[gmv|GMV]] (gross variant), reconciliation against [[payments]].

## Notes
- **Refunds do not decrement.** For net cash collected, use `SUM([[payments__amount_cents|payments.amount_cents]]) WHERE status='captured'`.
- A divergence between `total_cents` and `SUM(order_items.quantity * unit_price_cents)` for the same `order_id` indicates data corruption — flag for investigation.
