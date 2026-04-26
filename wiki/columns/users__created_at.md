---
type: column
name: users.created_at
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [stable]
last_updated: 2026-04-26
---

# users.created_at

**Type:** `TIMESTAMPTZ` · **Nullable:** no · **Default:** `now()`

**Definition.** When the user account was created (signup time). Stored with timezone; UTC in practice.

## Belongs to
[[users]]

## Lineage
- **Produced by:** DB default at INSERT.
- **Consumed by:** cohort analyses, retention curves, [[gmv|GMV]] new-user splits.

## Notes
- Stable — never updated after insert.
