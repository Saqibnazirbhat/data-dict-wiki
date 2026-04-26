---
type: column
name: payments.currency
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [finance, stable]
last_updated: 2026-04-26
---

# payments.currency

**Type:** `CHAR(3)` · **Nullable:** no · **Default:** `'USD'`

**Definition.** Currency for [[payments__amount_cents|amount_cents]], as ISO 4217.

## Belongs to
[[payments]]

## Notes
- Should match [[orders__currency|orders.currency]] for the same `order_id`. A mismatch is a data-quality alert raised by [[payments_reconciliation_dag]].
