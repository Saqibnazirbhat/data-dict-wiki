---
type: column
name: order_items.quantity
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [stable]
last_updated: 2026-04-26
---

# order_items.quantity

**Type:** `INTEGER` · **Nullable:** no · **CHECK:** `> 0`

**Definition.** Number of units of [[order_items__product_id|product]] purchased on this line.

## Belongs to
[[order_items]]

## Notes
- Must be strictly positive; refunds are modeled in [[payments]] with negative `amount_cents`, not by zero/negative quantities here.
