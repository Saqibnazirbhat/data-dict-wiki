---
type: column
name: orders.placed_at
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [stable]
last_updated: 2026-04-26
---

# orders.placed_at

**Type:** `TIMESTAMPTZ` · **Nullable:** no · **Default:** `now()` · **Indexed:** `orders_placed_at_idx`

**Definition.** When the order was created (checkout completed).

## Belongs to
[[orders]]

## Lineage
- **Consumed by:** date-bucketed [[gmv|GMV]] reporting, cohort analyses, [[order-lifecycle|order lifecycle]] duration metrics.

## Notes
- This is the *placement* time, not the payment-capture time. For revenue recognition timing, see [[payments__processed_at|payments.processed_at]].
