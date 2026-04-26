---
type: table
name: categories
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [product, stable]
last_updated: 2026-04-26
---

# categories

**Product taxonomy.** Self-referential tree via `parent_id` (NULL = top-level node). Used to roll product sales up by category in BI.

## Grain
One row per category node in the taxonomy. Surrogate key: `id`. No natural key (multiple sibling categories may share `name` under different parents).

## Columns
| Column | Type | Description |
| --- | --- | --- |
| [[categories__id\|id]] | `BIGSERIAL` PK | Surrogate category id. |
| [[categories__name\|name]] | `TEXT` | Display name (not unique). |
| [[categories__parent_id\|parent_id]] | `BIGINT` FK → [[categories]] | Self-reference; NULL for top-level. |
| [[categories__created_at\|created_at]] | `TIMESTAMPTZ` | Creation timestamp. |

## Upstream
- Merchandising team writes via admin panel.
- Source DDL: `raw/schemas/sample_ecommerce.sql`.

## Downstream
- [[products]] references `categories.id` via `products.category_id`.

## Notes
- Tree is shallow in practice (≤4 levels per merchandising convention). No DB-level depth constraint.
