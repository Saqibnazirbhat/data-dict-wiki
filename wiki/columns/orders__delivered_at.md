---
type: column
name: orders.delivered_at
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [ops, stable]
last_updated: 2026-04-26
---

# orders.delivered_at

**Type:** `TIMESTAMPTZ` · **Nullable:** yes (NULL until delivery)

**Definition.** When the carrier confirmed delivery to the customer.

## Belongs to
[[orders]]

## Lineage
- **Produced by:** shipping integration webhook (carrier delivery event).

## Notes
- The transition `shipped` → `delivered` is what flips [[orders__status|status]] to `delivered`.
- Some carriers backfill this hours/days late — analyses sensitive to delivery time should allow a lag.
