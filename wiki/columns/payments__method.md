---
type: column
name: payments.method
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [finance, stable]
last_updated: 2026-04-26
---

# payments.method

**Type:** `TEXT` · **Nullable:** no

**Definition.** The payment instrument used.

## Belongs to
[[payments]]

## Allowed values / domain
- `card` — credit/debit card via Stripe/Adyen.
- `paypal`
- `apple_pay`
- `gift_card` — internal store credit.
- `bank_transfer` — ACH / SEPA.

## Notes
- Not a DB enum — app-validated. New methods added without schema change.
