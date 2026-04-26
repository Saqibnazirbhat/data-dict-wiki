---
type: column
name: categories.parent_id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# categories.parent_id

**Type:** `BIGINT` · **Nullable:** yes (NULL = top-level) · **FK** → [[categories__id|categories.id]]

**Definition.** Self-referential parent for the taxonomy tree. NULL means this is a top-level (root) category.

## Belongs to
[[categories]]

## Lineage
- **References:** [[categories__id|categories.id]] (same table).

## Notes
- No DB-level depth limit; merchandising convention caps at ≤4 levels.
- No cycle prevention — relies on app discipline.
