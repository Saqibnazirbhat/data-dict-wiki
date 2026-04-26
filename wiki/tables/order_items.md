---
type: table
name: order_items
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [finance, stable]
last_updated: 2026-04-26
---

# order_items

**Line items inside an [[orders|order]].** `quantity * unit_price_cents` summed across an order's items reconciles to [[orders__total_cents|orders.total_cents]] at placement time (not after).

## Grain
One row per (order, product) line. Surrogate key: `id`. Note: the same product can appear multiple times in one order if added separately — there is no UNIQUE on (order_id, product_id).

## Columns
| Column | Type | Description |
| --- | --- | --- |
| [[order_items__id\|id]] | `BIGSERIAL` PK | Surrogate line-item id. |
| [[order_items__order_id\|order_id]] | `BIGINT` FK → [[orders]] | Owning order. `ON DELETE CASCADE`. |
| [[order_items__product_id\|product_id]] | `BIGINT` FK → [[products]] | The product purchased. |
| [[order_items__quantity\|quantity]] | `INTEGER` >0 | Units purchased on this line. |
| [[order_items__unit_price_cents\|unit_price_cents]] | `INTEGER` ≥0 | **Snapshot** of [[products__price_cents\|products.price_cents]] at order time. |

## Upstream
- Written transactionally with the parent [[orders]] row at checkout.
- Source DDL: `raw/schemas/sample_ecommerce.sql`.

## Downstream
- Joined to [[products]] and [[categories]] for category-level revenue analysis.
- Feeds [[orders_daily_pipeline]].

## Notes
- **Price snapshot.** `unit_price_cents` is the historically-correct price. Do not join to current [[products__price_cents]] for past orders — you'll get drift.
- `ON DELETE CASCADE` from [[orders]]: deleting an order removes its line items.
