---
type: table
name: orders
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [finance, ops, stable]
last_updated: 2026-04-26
---

# orders

**The cart envelope** — one row per customer order, not per line item. See [[order_items]] for line-item detail. `total_cents` is denormalized at placement time and **does not** reflect later refunds; for actual money movement, see [[payments]].

## Grain
One row per placed order. Surrogate key: `id`. No natural business key.

## Columns
| Column | Type | Description |
| --- | --- | --- |
| [[orders__id\|id]] | `BIGSERIAL` PK | Surrogate order id. |
| [[orders__user_id\|user_id]] | `BIGINT` FK → [[users]] | Customer who placed the order. |
| [[orders__status\|status]] | `TEXT` | Lifecycle state — see [[order-lifecycle\|order lifecycle]]. |
| [[orders__total_cents\|total_cents]] | `BIGINT` ≥0 | Sum of line items at placement. Frozen. |
| [[orders__currency\|currency]] | `CHAR(3)` | ISO 4217. Default `USD`. |
| [[orders__placed_at\|placed_at]] | `TIMESTAMPTZ` | Order creation time. |
| [[orders__shipped_at\|shipped_at]] | `TIMESTAMPTZ` NULL | Set when carrier accepts shipment. |
| [[orders__delivered_at\|delivered_at]] | `TIMESTAMPTZ` NULL | Set when carrier confirms delivery. |

## Upstream
- Application checkout flow writes a row + N [[order_items]] rows in a single transaction.
- Source DDL: `raw/schemas/sample_ecommerce.sql`.

## Downstream
- [[order_items]] FK → `orders.id` (CASCADE on delete).
- [[payments]] FK → `orders.id` (one order, many payment attempts).
- [[orders_daily_pipeline]] aggregates this table into `mart.orders_daily`.
- Powers [[gmv|GMV]], [[order-lifecycle|order lifecycle]], [[revenue-recognition|revenue recognition]].

## Notes
- **`total_cents` is frozen.** Refunds do not decrement it. To compute net revenue, sum [[payments__amount_cents|payments.amount_cents]] WHERE `status='captured'` (refunds appear as negative amounts).
- `status` enum: `pending` → `paid` → `shipped` → `delivered`, with terminal states `cancelled` and `refunded`. Documented in [[order-lifecycle|order lifecycle]].
