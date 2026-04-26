---
type: column
name: products.price_cents
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [finance, stable]
last_updated: 2026-04-26
---

# products.price_cents

**Type:** `INTEGER` · **Nullable:** no · **CHECK:** `>= 0`

**Definition.** Current list price in minor units of [[products__currency|currency]] (cents for USD, paise for INR, etc.). Integer storage avoids floating-point money math.

## Belongs to
[[products]]

## Lineage
- **Produced by:** merchandising admin / vendor price feed.
- **Consumed by:** **NOT** historical orders — those use [[order_items__unit_price_cents|order_items.unit_price_cents]] (price snapshot at order time).

## Notes
- This column reflects *current* list price only. Price history is not versioned in this table.
