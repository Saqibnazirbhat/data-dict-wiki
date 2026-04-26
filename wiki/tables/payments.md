---
type: table
name: payments
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [finance, pci, stable]
last_updated: 2026-04-26
---

# payments

**Every payment attempt against an [[orders|order]].** An order can have many payments (retries, partial captures, refunds). Money has actually moved **only when `status='captured'`**. Refunds appear as rows with negative `amount_cents`.

## Grain
One row per payment event (authorize / capture / fail / refund). Surrogate key: `id`. Reconcile with the processor via `processor_ref`.

## Columns
| Column | Type | Description |
| --- | --- | --- |
| [[payments__id\|id]] | `BIGSERIAL` PK | Surrogate payment id. |
| [[payments__order_id\|order_id]] | `BIGINT` FK → [[orders]] | Order being paid for. |
| [[payments__method\|method]] | `TEXT` | `card` / `paypal` / `apple_pay` / `gift_card` / `bank_transfer`. |
| [[payments__amount_cents\|amount_cents]] | `BIGINT` | **Signed.** Negative for refunds. |
| [[payments__currency\|currency]] | `CHAR(3)` | ISO 4217. Default `USD`. |
| [[payments__status\|status]] | `TEXT` | `authorized` / `captured` / `failed` / `refunded`. |
| [[payments__processor_ref\|processor_ref]] | `TEXT` | Stripe/Adyen transaction id — the source of truth. |
| [[payments__processed_at\|processed_at]] | `TIMESTAMPTZ` | When the processor confirmed the event. |

## Upstream
- Application payment service writes on each processor webhook.
- Source DDL: `raw/schemas/sample_ecommerce.sql`.

## Downstream
- [[payments_reconciliation_dag]] reconciles this table nightly against processor exports.
- Powers [[revenue-recognition|revenue recognition]] (only `status='captured'` rows count) and [[gmv|GMV]] (the actual-cash variant).

## Notes
- **PCI.** Never store raw card data here — only `processor_ref` (the processor's tokenized id).
- **Signed amounts.** Filtering `WHERE amount_cents > 0` excludes refunds; for net revenue use `SUM(amount_cents) WHERE status='captured'`.
- An order's `status='paid'` is set only when the *sum* of captured payments ≥ [[orders__total_cents|orders.total_cents]] (handled by application, not DB constraint).
