---
type: column
name: payments.status
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [finance, stable]
last_updated: 2026-04-26
---

# payments.status

**Type:** `TEXT` · **Nullable:** no · **Indexed:** `payments_status_idx`

**Definition.** Outcome of the payment event from the processor.

## Belongs to
[[payments]]

## Allowed values / domain
- `authorized` — funds reserved, not yet moved.
- `captured` — funds actually collected. **The only status that counts as real revenue.**
- `failed` — declined / errored.
- `refunded` — corresponds to a negative-[[payments__amount_cents|amount_cents]] row.

## Notes
- Not a DB enum.
- For [[revenue-recognition|revenue recognition]], `status='captured'` is the only filter that should be used.
