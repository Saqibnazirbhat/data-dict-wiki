---
type: column
name: products.status
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [stable]
last_updated: 2026-04-26
---

# products.status

**Type:** `TEXT` · **Nullable:** no · **Default:** `'active'`

**Definition.** Whether the product is currently sellable.

## Belongs to
[[products]]

## Allowed values / domain
- `active` — appears in catalog, can be ordered.
- `discontinued` — hidden from catalog. Existing [[order_items|order_items]] still reference it.

## Notes
- Not a DB enum — app-validated only.
- Discontinuing does not delete: historical order data remains intact.
