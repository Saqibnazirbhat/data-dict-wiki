---
type: column
name: products.currency
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [finance, stable]
last_updated: 2026-04-26
---

# products.currency

**Type:** `CHAR(3)` · **Nullable:** no · **Default:** `'USD'`

**Definition.** Currency in which [[products__price_cents|price_cents]] is denominated, as ISO 4217.

## Belongs to
[[products]]

## Allowed values / domain
ISO 4217 alpha-3 (e.g. `USD`, `EUR`, `INR`). Not validated at DB level.

## Notes
- Multi-currency catalog requires a separate `product_prices` table per currency; this column captures the *primary* listing currency only.
