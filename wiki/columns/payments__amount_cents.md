---
type: column
name: payments.amount_cents
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [finance, stable]
last_updated: 2026-04-26
---

# payments.amount_cents

**Type:** `BIGINT` · **Nullable:** no · **Signed**

**Definition.** Amount of this payment event in minor units of [[payments__currency|currency]]. **Signed:** positive for captures/auths, **negative for refunds**.

## Belongs to
[[payments]]

## Lineage
- **Produced by:** processor webhook payload.
- **Consumed by:** [[revenue-recognition|revenue recognition]], [[gmv|GMV]] (cash variant), reconciliation by [[payments_reconciliation_dag]].

## Notes
- For net cash collected on an order: `SUM(amount_cents) WHERE order_id = X AND status='captured'`.
- Filtering `> 0` excludes refunds — choose deliberately.
