---
type: column
name: order_items.product_id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# order_items.product_id

**Type:** `BIGINT` · **Nullable:** no · **FK** → [[products__id|products.id]] · **Indexed:** `order_items_product_idx`

**Definition.** The product purchased on this line.

## Belongs to
[[order_items]]

## Lineage
- **References:** [[products__id|products.id]].

## Notes
- No `(order_id, product_id)` UNIQUE — same product may appear multiple times in one order.
- Joins to a [[products|product]] that may have since been [[products__status|discontinued]].
