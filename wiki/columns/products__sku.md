---
type: column
name: products.sku
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [stable]
last_updated: 2026-04-26
---

# products.sku

**Type:** `TEXT` · **Nullable:** no · **UNIQUE**

**Definition.** Vendor-provided Stock Keeping Unit. The natural key for [[products]].

## Belongs to
[[products]]

## Lineage
- **Produced by:** vendor catalog imports / merchandising admin.

## Allowed values / domain
Free-form vendor string; uniqueness enforced at DB.

## Notes
- Two products with the same physical good but different vendors will have different SKUs.
