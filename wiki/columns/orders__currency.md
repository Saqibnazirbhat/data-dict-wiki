---
type: column
name: orders.currency
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [finance, stable]
last_updated: 2026-04-26
---

# orders.currency

**Type:** `CHAR(3)` · **Nullable:** no · **Default:** `'USD'`

**Definition.** Currency for [[orders__total_cents|total_cents]], as ISO 4217.

## Belongs to
[[orders]]

## Notes
- Multi-currency aggregations require FX conversion to a reporting currency — handled by [[orders_daily_pipeline]].
