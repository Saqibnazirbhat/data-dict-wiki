---
type: column
name: products.name
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# products.name

**Type:** `TEXT` · **Nullable:** no

**Definition.** Customer-facing product display name.

## Belongs to
[[products]]

## Lineage
- **Produced by:** merchandising admin panel / vendor import.

## Notes
- May be edited; not versioned. For historical naming, refer to order/email snapshots.
