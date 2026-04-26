---
type: concept
name: Order Lifecycle
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [ops, lifecycle]
last_updated: 2026-04-26
---

# Order Lifecycle

**The state machine an order moves through from checkout to terminal state.** Encoded in [[orders__status|orders.status]] with timestamp markers ([[orders__placed_at|placed_at]], [[orders__shipped_at|shipped_at]], [[orders__delivered_at|delivered_at]]).

## States and transitions

```
                                   ┌──────────────┐
                          ┌──────► │  cancelled   │   (terminal)
                          │        └──────────────┘
                          │
   pending  ─────►  paid  ────►  shipped  ────►  delivered   (terminal)
      │                                  │
      │                                  └────►  refunded    (terminal)
      └────────────►  cancelled   (terminal, before payment)
```

| State | Set by | Timestamp | Notes |
| --- | --- | --- | --- |
| `pending` | checkout (default) | [[orders__placed_at\|placed_at]] | Awaiting payment. |
| `paid` | payment service | — | Sum of captured [[payments]] ≥ [[orders__total_cents\|total_cents]]. |
| `shipped` | shipping integration | [[orders__shipped_at\|shipped_at]] | Carrier accepted shipment. |
| `delivered` | shipping integration | [[orders__delivered_at\|delivered_at]] | Carrier confirmed delivery. |
| `cancelled` | app / admin | — | May be reached from `pending` or `paid`. |
| `refunded` | refund flow | — | Net captured payments == 0 (refunds offset captures). |

## Computed from
- [[orders__status|orders.status]] + the three timestamp columns.
- Cross-checked against [[payments]] for `paid` / `refunded`.

## Related concepts
[[gmv|GMV]], [[revenue-recognition|revenue recognition]]

## Open questions / contradictions
- _None currently._
