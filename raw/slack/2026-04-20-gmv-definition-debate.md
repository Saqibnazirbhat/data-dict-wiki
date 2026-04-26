# Slack — #data-platform — 2026-04-20 — GMV definition disagreement

Exported thread. Participants: Maya (Finance), David (Data Platform), Priya (Growth).

---

**Maya — Finance · 14:02**
> Quick Q for #data — the GMV number on the BI dashboard for Q1 came in at $14.2M, but our finance close booked $13.6M. Delta is bigger than I'd expect from refund timing alone. Are we using the same definition?

**David — Data Platform · 14:08**
> The BI dashboard uses gross GMV: `SUM(orders.total_cents)` over orders with status in (`paid`, `shipped`, `delivered`) and `placed_at` in the period. That's the historical definition we shipped with — `orders.total_cents` is frozen at placement and doesn't move on refund.

**Maya — Finance · 14:11**
> Right, that's the issue. Finance books revenue when payment is captured, not when the order is placed. We use `SUM(payments.amount_cents) WHERE status='captured'` keyed on `processed_at` for the period. Refunds (negative `amount_cents`) reduce that number; gross GMV doesn't subtract them. Different number, different timing, different denominator.

**David — Data Platform · 14:15**
> Agreed, two definitions. We've been calling them gross GMV (placement-time, what BI shows) and net cash GMV (capture-time, what Finance books). Both are real numbers, depending on the question.

**Maya — Finance · 14:18**
> For Finance, "GMV" means net cash — that's the canonical number for the board deck. Anyone showing gross should label it as such, otherwise we end up explaining the same delta every quarter close. Can we get the wiki to make that explicit?

**David — Data Platform · 14:21**
> Yes — I'll get someone to update the GMV concept page. We're not going to silently change the BI dashboard's GMV column though, that breaks too many downstream reports.

**Priya — Growth · 14:30**
> +1 Growth needs the dashboard to keep showing gross. Net cash isn't the right number for the weekly review — we need the placed-but-uncollected portion to size the funnel and measure conversion. Different team, different definition, both legitimate.

---

## Outcome

- **Resolved:** Wiki [[gmv]] page must document both definitions, name them, and explicitly call out which team uses which.
- **Open:** Whether the BI dashboard's "GMV" column should be relabeled "Gross GMV" or split into two columns. Owner: BI team. No deadline set.
- **Action item (David, Data Platform):** Update wiki `gmv` page. Done 2026-04-20.

## Canonical definitions (per this thread)

- **Gross GMV (placement-time)** — Growth/BI canonical. `SUM(orders.total_cents)` keyed on `placed_at`, status filter (`paid`, `shipped`, `delivered`). Does not subtract refunds.
- **Net cash GMV (capture-time)** — Finance canonical. `SUM(payments.amount_cents) WHERE status='captured'` keyed on `processed_at`. Refunds (negative amounts) subtract.
