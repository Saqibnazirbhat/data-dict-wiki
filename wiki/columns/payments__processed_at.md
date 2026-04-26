---
type: column
name: payments.processed_at
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [finance, stable]
last_updated: 2026-04-26
---

# payments.processed_at

**Type:** `TIMESTAMPTZ` · **Nullable:** no · **Default:** `now()`

**Definition.** When the processor confirmed the payment event.

## Belongs to
[[payments]]

## Lineage
- **Consumed by:** [[revenue-recognition|revenue recognition]] (the date that determines the booking period), [[payments_reconciliation_dag]].

## Notes
- Use this — not [[orders__placed_at|orders.placed_at]] — when the question is "when did money actually move?".
