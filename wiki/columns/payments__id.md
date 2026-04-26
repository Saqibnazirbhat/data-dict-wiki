---
type: column
name: payments.id
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# payments.id

**Type:** `BIGSERIAL` · **Nullable:** no · **PRIMARY KEY**

**Definition.** Surrogate primary key for a payment event row.

## Belongs to
[[payments]]

## Notes
- Surrogate; the *processor's* transaction id lives in [[payments__processor_ref|processor_ref]].
