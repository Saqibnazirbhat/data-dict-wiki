---
type: column
name: payments.processor_ref
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [pci, finance, stable]
last_updated: 2026-04-26
---

# payments.processor_ref

**Type:** `TEXT` · **Nullable:** no

**Definition.** Opaque transaction id from the upstream processor (Stripe, Adyen, …). The reconciliation key against the processor's own ledger.

## Belongs to
[[payments]]

## Lineage
- **Produced by:** processor webhook payload.
- **Consumed by:** [[payments_reconciliation_dag]] — joins on this to verify our row matches the processor's record.

## Notes
- **PCI.** This is a tokenized reference, *not* a card number. Never put raw PAN or card data here.
