---
type: column
name: orders.id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [stable]
last_updated: 2026-04-26
---

# orders.id

**Type:** `BIGSERIAL` · **Nullable:** no · **PRIMARY KEY**

**Definition.** Surrogate primary key for an order.

## Belongs to
[[orders]]

## Lineage
- **Produced by:** checkout transaction (DB-assigned).
- **Consumed by:** [[order_items__order_id|order_items.order_id]] (CASCADE), [[payments__order_id|payments.order_id]].

## Notes
- Not the customer-facing order number. (No customer-facing order number is modeled in this schema.)
