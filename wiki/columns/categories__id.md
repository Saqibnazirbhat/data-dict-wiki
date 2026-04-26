---
type: column
name: categories.id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [stable]
last_updated: 2026-04-26
---

# categories.id

**Type:** `BIGSERIAL` · **Nullable:** no · **PRIMARY KEY**

**Definition.** Surrogate primary key for a category node.

## Belongs to
[[categories]]

## Lineage
- **Produced by:** admin panel (DB-assigned).
- **Consumed by:** [[categories__parent_id|categories.parent_id]] (self-FK), [[products__category_id|products.category_id]].

## Notes
- Stable; never recycled.
