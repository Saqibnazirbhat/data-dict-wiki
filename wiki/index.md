---
type: index
last_updated: 2026-04-26
---

# Data Dictionary & Lineage Wiki

Canonical, human-readable documentation for the data stack. See [[CLAUDE|operating manual]] for conventions.

## Counts
- Tables: **6**
- Columns: **40**
- Pipelines: **2** (both stubs)
- Concepts: **3**
- Owners: **2**

## Tables
- [[categories]] — Product taxonomy. Self-referential tree.
- [[order_items]] — Line items inside an order. Price-snapshot at order time.
- [[orders]] — The cart envelope. One row per placed order.
- [[payments]] — Every payment attempt against an order. Signed amounts.
- [[products]] — Catalog of sellable items. SKU is the natural key.
- [[users]] — Every person who has ever signed up. PII; soft-deleted.

## Columns

### users
- [[users__country]] — Signup country, ISO 3166-1 alpha-2.
- [[users__created_at]] — Signup timestamp.
- [[users__deleted_at]] — GDPR delete timestamp; NULL when active.
- [[users__email]] — Login identifier and natural key. PII.
- [[users__id]] — Surrogate PK.
- [[users__name]] — Display name. PII.
- [[users__status]] — `active` / `suspended` / `deleted`.

### categories
- [[categories__created_at]] — Creation timestamp.
- [[categories__id]] — Surrogate PK.
- [[categories__name]] — Display name (not unique).
- [[categories__parent_id]] — Self-FK; NULL for top-level.

### products
- [[products__category_id]] — FK to [[categories]].
- [[products__created_at]] — Creation timestamp.
- [[products__currency]] — ISO 4217 for `price_cents`.
- [[products__id]] — Surrogate PK.
- [[products__name]] — Customer-facing name.
- [[products__price_cents]] — Current list price; not historical.
- [[products__sku]] — Vendor SKU; natural key.
- [[products__status]] — `active` / `discontinued`.

### orders
- [[orders__currency]] — ISO 4217 for `total_cents`.
- [[orders__delivered_at]] — Carrier delivery confirmation.
- [[orders__id]] — Surrogate PK.
- [[orders__placed_at]] — Order creation time.
- [[orders__shipped_at]] — Carrier acceptance time.
- [[orders__status]] — Lifecycle state; see [[order-lifecycle|order lifecycle]].
- [[orders__total_cents]] — Frozen total at placement; not net-of-refunds.
- [[orders__user_id]] — FK to [[users]].

### order_items
- [[order_items__id]] — Surrogate PK.
- [[order_items__order_id]] — FK to [[orders]] (CASCADE).
- [[order_items__product_id]] — FK to [[products]].
- [[order_items__quantity]] — Units; strictly positive.
- [[order_items__unit_price_cents]] — Snapshot of [[products__price_cents]] at order time.

### payments
- [[payments__amount_cents]] — Signed; negative for refunds.
- [[payments__currency]] — ISO 4217.
- [[payments__id]] — Surrogate PK.
- [[payments__method]] — `card` / `paypal` / etc.
- [[payments__order_id]] — FK to [[orders]].
- [[payments__processed_at]] — Processor confirmation time.
- [[payments__processor_ref]] — Tokenized processor txn id.
- [[payments__status]] — `authorized` / `captured` / `failed` / `refunded`.

## Pipelines
- [[orders_daily_pipeline]] — Daily aggregation of [[orders]] + [[order_items]] into `mart.orders_daily`. **Stub.**
- [[payments_reconciliation_dag]] — Nightly reconciliation against processor settlement. **Stub.**

## Concepts
- [[gmv|GMV]] — Gross Merchandise Value. Two variants (placement vs cash).
- [[order-lifecycle|Order Lifecycle]] — State machine over [[orders__status]].
- [[revenue-recognition|Revenue Recognition]] — When/how much revenue gets booked.

## Owners
- [[data-platform-team|Data Platform team]] — Warehouse + canonical models.
- [[growth-team|Growth team]] — Acquisition + lifecycle; product-side owner of [[users]].

## Stubs awaiting fill
- [[orders_daily_pipeline]] — needs dbt model SQL in `raw/pipelines/`.
- [[payments_reconciliation_dag]] — needs DAG file in `raw/pipelines/`.

## Open questions
- [[revenue-recognition]] — exact "shipped vs delivered" recognition trigger needs Finance sign-off.

## Recently updated
All pages last_updated **2026-04-26** (initial ingest).
