---
type: concept
name: Revenue Recognition
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [finance, metric]
last_updated: 2026-04-26
---

# Revenue Recognition

**The rules for *when* and *how much* revenue gets booked from an order.** Distinct from [[gmv|GMV]] (a top-line activity number) — this is the number Finance uses for the books.

## Rule of thumb (engineering view)

A payment row counts toward recognized revenue when:
1. [[payments__status|payments.status]] = `'captured'` (real money moved), AND
2. The associated [[orders|order]] has reached a state in which the goods/service was actually delivered (`shipped` or `delivered`, depending on policy).

The booking date is [[payments__processed_at|payments.processed_at]], not [[orders__placed_at|orders.placed_at]].

Refunds (negative [[payments__amount_cents|amount_cents]]) reverse recognized revenue in the period they were processed, not the period of the original sale.

## Computed from
- [[payments]] (status, amount, processed_at)
- [[orders]] (status — gates whether revenue can be recognized)

## Related concepts
[[gmv|GMV]], [[order-lifecycle|order lifecycle]]

## Open questions / contradictions
- The exact "shipped vs delivered" trigger for recognition needs Finance sign-off — the schema supports either, but the BI layer currently uses `shipped`. Tagged `needs-info` for now.
