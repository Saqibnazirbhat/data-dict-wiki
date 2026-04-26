---
type: column
name: order_items.unit_price_cents
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [finance, stable]
last_updated: 2026-04-26
---

# order_items.unit_price_cents

**Type:** `INTEGER` · **Nullable:** no · **CHECK:** `>= 0`

**Definition.** **Snapshot** of [[products__price_cents|products.price_cents]] at the moment the order was placed. The historically-correct unit price.

## Belongs to
[[order_items]]

## Lineage
- **Produced by:** checkout — copied from [[products__price_cents|products.price_cents]] at INSERT.
- **Consumed by:** [[gmv|GMV]], any historical revenue analysis.

## Notes
- **Do not** join to current [[products__price_cents]] for past orders — prices drift. Always use this snapshot.
- Currency is implicitly the parent order's [[orders__currency|currency]].
