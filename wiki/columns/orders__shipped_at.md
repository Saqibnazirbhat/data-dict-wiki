---
type: column
name: orders.shipped_at
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [ops, stable]
last_updated: 2026-04-26
---

# orders.shipped_at

**Type:** `TIMESTAMPTZ` · **Nullable:** yes (NULL until shipment)

**Definition.** When the carrier accepted the shipment.

## Belongs to
[[orders]]

## Lineage
- **Produced by:** shipping integration webhook.
- **Consumed by:** fulfillment SLA dashboards.

## Notes
- NULL for any order in `pending`, `paid`, `cancelled` states; should be set when [[orders__status|status]] transitions to `shipped`.
