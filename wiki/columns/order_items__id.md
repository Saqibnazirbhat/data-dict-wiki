---
type: column
name: order_items.id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# order_items.id

**Type:** `BIGSERIAL` · **Nullable:** no · **PRIMARY KEY**

**Definition.** Surrogate primary key for an order line item.

## Belongs to
[[order_items]]

## Notes
- Stable; never recycled.
