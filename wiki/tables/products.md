---
type: table
name: products
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [product, finance, stable]
last_updated: 2026-04-26
---

# products

**Catalog of sellable items.** A product belongs to exactly one [[categories|category]]. Soft-deleted via `status='discontinued'`. `price_cents` is integer to avoid floating-point math on money.

## Grain
One row per product. Natural key: `sku` (UNIQUE, vendor-provided). Surrogate key: `id`.

## Columns
| Column | Type | Description |
| --- | --- | --- |
| [[products__id\|id]] | `BIGSERIAL` PK | Surrogate product id. |
| [[products__sku\|sku]] | `TEXT` UNIQUE | Vendor SKU; the natural key. |
| [[products__name\|name]] | `TEXT` | Display name. |
| [[products__category_id\|category_id]] | `BIGINT` FK → [[categories]] | Owning category. |
| [[products__price_cents\|price_cents]] | `INTEGER` ≥0 | List price in minor units. |
| [[products__currency\|currency]] | `CHAR(3)` | ISO 4217 currency code. Default `USD`. |
| [[products__status\|status]] | `TEXT` | `active` / `discontinued`. |
| [[products__created_at\|created_at]] | `TIMESTAMPTZ` | Creation timestamp. |

## Upstream
- Merchandising/Catalog team writes via admin panel and bulk vendor imports.
- Source DDL: `raw/schemas/sample_ecommerce.sql`.

## Downstream
- [[order_items]] references `products.id` via `order_items.product_id`.
- [[order_items__unit_price_cents|unit_price_cents]] is a *snapshot* of `products.price_cents` at order time (do not join back for historical pricing).

## Notes
- Price changes are not versioned in this table; the [[order_items]] snapshot is the historical record.
