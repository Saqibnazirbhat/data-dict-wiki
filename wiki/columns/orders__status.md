---
type: column
name: orders.status
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [ops, stable]
last_updated: 2026-04-26
---

# orders.status

**Type:** `TEXT` · **Nullable:** no · **Default:** `'pending'` · **Indexed:** `orders_status_idx`

**Definition.** Lifecycle state of the order. The progression is documented in [[order-lifecycle|order lifecycle]].

## Belongs to
[[orders]]

## Lineage
- **Produced by:** application state machine (checkout, payment service, shipping integration).
- **Consumed by:** ops dashboards, [[gmv|GMV]] (typically counts only `paid`+ states), refund analytics.

## Allowed values / domain
- `pending` — order placed, awaiting payment.
- `paid` — captured payment ≥ [[orders__total_cents|total_cents]] (set by app, not DB constraint).
- `shipped` — handed to carrier; [[orders__shipped_at|shipped_at]] set.
- `delivered` — carrier confirmed delivery; [[orders__delivered_at|delivered_at]] set.
- `cancelled` — terminal; cancelled before shipment.
- `refunded` — terminal; full refund issued (see [[payments]]).

## Notes
- Not a DB enum — app-validated.
- See [[order-lifecycle|order lifecycle]] for the full state diagram.
