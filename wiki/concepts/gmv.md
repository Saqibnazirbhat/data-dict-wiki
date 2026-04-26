---
type: concept
name: GMV (Gross Merchandise Value)
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql, raw/slack/2026-04-20-gmv-definition-debate.md]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f, raw/slack/2026-04-20-gmv-definition-debate.md: d3845126cec6d675}
tags: [finance, metric, disputed]
last_updated: 2026-04-26
---

# GMV (Gross Merchandise Value)

**Total monetary value of orders, by some definition.** The headline top-line metric for the business — but there is no single canonical definition. Two variants are in active use, and **the same word "GMV" means different numbers to different teams** (per `raw/slack/2026-04-20-gmv-definition-debate.md`). Always be explicit about which you mean.

## Variants

### Gross GMV (placement-time)
`SUM([[orders__total_cents|orders.total_cents]])` over orders with [[orders__placed_at|placed_at]] in the period and [[orders__status|status]] in (`paid`, `shipped`, `delivered`).

- **Materialized as:** [[orders_daily__gmv_gross_cents|orders_daily.gmv_gross_cents]] in [[orders_daily|mart.orders_daily]], computed by [[orders_daily_pipeline]].
- **Canonical for:** BI dashboards, [[growth-team|Growth team]] weekly review (sizes the funnel including placed-but-uncollected orders).
- **Refund handling:** does not subtract refunds. [[orders__total_cents|orders.total_cents]] is frozen at placement.

### Net cash GMV (capture-time)
`SUM([[payments__amount_cents|payments.amount_cents]])` over [[payments]] rows with [[payments__processed_at|processed_at]] in the period and [[payments__status|status]] = `'captured'`.

- **Canonical for:** Finance close, board deck.
- **Refund handling:** refunds appear as negative [[payments__amount_cents|amount_cents]] and reduce the total.

## Computed from
- [[orders]] / [[orders_daily]] (gross variant)
- [[payments]] (net cash variant)

## Related concepts
[[order-lifecycle|order lifecycle]], [[revenue-recognition|revenue recognition]]

## Notes

**CONTRADICTION:** "GMV" means different things to different teams (per `raw/slack/2026-04-20-gmv-definition-debate.md`, 2026-04-20):

- **Finance** (Maya) — "GMV" is **net cash** (capture-time). This is the canonical number for the board deck. Anything labelled "GMV" without qualification should be net cash.
- **Data Platform / BI** (David) — historical BI dashboard implementation is **gross** (placement-time). Documented and shipped years ago.
- **Growth** (Priya) — needs the **gross** number for weekly review; net cash is the wrong shape for funnel sizing.

**Resolution:** the wiki documents both definitions side-by-side and names which team uses which. The BI dashboard's "GMV" column has not been renamed (decision deferred to BI team — affects too many downstream reports). When citing a GMV figure, always specify gross vs net cash.

**Open:** whether the BI dashboard column should be relabelled "Gross GMV" or split into two columns. No deadline; owner: BI team.
