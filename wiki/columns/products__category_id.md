---
type: column
name: products.category_id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [stable]
last_updated: 2026-04-26
---

# products.category_id

**Type:** `BIGINT` · **Nullable:** no · **FK** → [[categories__id|categories.id]] · **Indexed:** `products_category_idx`

**Definition.** The single category this product is filed under.

## Belongs to
[[products]]

## Lineage
- **References:** [[categories__id|categories.id]].
- **Consumed by:** category-level revenue rollups (via [[order_items]] join).

## Notes
- One-to-many: a product belongs to exactly one category. Multi-category needs a separate join table (not modeled here).
