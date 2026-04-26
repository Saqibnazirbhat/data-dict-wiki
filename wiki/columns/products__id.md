---
type: column
name: products.id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# products.id

**Type:** `BIGSERIAL` · **Nullable:** no · **PRIMARY KEY**

**Definition.** Surrogate primary key for a product. Stable for the lifetime of the row, including discontinuation.

## Belongs to
[[products]]

## Lineage
- **Produced by:** admin panel / vendor import (DB-assigned).
- **Consumed by:** [[order_items__product_id|order_items.product_id]].

## Notes
- Never recycled.
