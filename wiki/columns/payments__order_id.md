---
type: column
name: payments.order_id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# payments.order_id

**Type:** `BIGINT` · **Nullable:** no · **FK** → [[orders__id|orders.id]] · **Indexed:** `payments_order_idx`

**Definition.** The order this payment event applies to.

## Belongs to
[[payments]]

## Lineage
- **References:** [[orders__id|orders.id]].

## Notes
- One order may have many payment rows (auth, capture, retries, refunds).
