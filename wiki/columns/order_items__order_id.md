---
type: column
name: order_items.order_id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# order_items.order_id

**Type:** `BIGINT` · **Nullable:** no · **FK** → [[orders__id|orders.id]] · **ON DELETE CASCADE** · **Indexed:** `order_items_order_idx`

**Definition.** The parent order this line item belongs to.

## Belongs to
[[order_items]]

## Lineage
- **References:** [[orders__id|orders.id]].

## Notes
- **CASCADE delete** — removing an order removes its line items.
