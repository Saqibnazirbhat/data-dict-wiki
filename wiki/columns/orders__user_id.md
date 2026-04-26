---
type: column
name: orders.user_id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# orders.user_id

**Type:** `BIGINT` · **Nullable:** no · **FK** → [[users__id|users.id]] · **Indexed:** `orders_user_idx`

**Definition.** The customer who placed this order.

## Belongs to
[[orders]]

## Lineage
- **References:** [[users__id|users.id]].
- **Consumed by:** all per-user revenue analyses, cohort retention, [[gmv|GMV]] segmented by user.

## Notes
- Guest checkout is not supported by this schema — every order has a user.
