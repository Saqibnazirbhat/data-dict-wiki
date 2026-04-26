---
type: concept
name: GMV (Gross Merchandise Value)
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [finance, metric]
last_updated: 2026-04-26
---

# GMV (Gross Merchandise Value)

**Total monetary value of orders placed in a period, before refunds and before subtracting cost of goods.** The headline top-line metric for the business. There are two common variants — be explicit about which you mean.

## Variants

### "Gross" GMV (placement-time)
`SUM([[orders__total_cents|orders.total_cents]])` over orders with [[orders__placed_at|placed_at]] in the period and [[orders__status|status]] in (`paid`, `shipped`, `delivered`).

This is the default the BI dashboards use. It does **not** subtract refunds.

### "Net cash" GMV (capture-time)
`SUM([[payments__amount_cents|payments.amount_cents]])` over [[payments]] rows with [[payments__processed_at|processed_at]] in the period and [[payments__status|status]] = `'captured'`.

Refunds (negative `amount_cents`) reduce this. This is closer to what the finance team books.

## Computed from
- [[orders]] (gross variant)
- [[payments]] (net cash variant)

## Related concepts
[[order-lifecycle|order lifecycle]], [[revenue-recognition|revenue recognition]]

## Open questions / contradictions
- _None currently._
