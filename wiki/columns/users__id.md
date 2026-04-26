---
type: column
name: users.id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# users.id

**Type:** `BIGSERIAL` · **Nullable:** no · **Default:** auto-increment · **PRIMARY KEY**

**Definition.** Surrogate primary key for a registered user. Stable for the lifetime of the row, including soft-deletion.

## Belongs to
[[users]]

## Lineage
- **Produced by:** application signup flow (DB-assigned).
- **Consumed by:** [[orders__user_id|orders.user_id]] (FK reference).

## Allowed values / domain
Positive 64-bit integer.

## Notes
- Never recycled, even after a user is hard-deleted.
