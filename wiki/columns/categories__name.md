---
type: column
name: categories.name
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# categories.name

**Type:** `TEXT` · **Nullable:** no

**Definition.** Display name of the category. Not unique — sibling categories under different parents may share a name (e.g. "Accessories" under both "Men" and "Women").

## Belongs to
[[categories]]

## Lineage
- **Produced by:** merchandising admin panel.

## Notes
- Use the (parent path, name) tuple as the human-readable identifier in BI.
