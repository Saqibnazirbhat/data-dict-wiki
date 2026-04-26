---
type: column
name: users.country
status: draft
owner: [[growth-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [stable]
last_updated: 2026-04-26
---

# users.country

**Type:** `CHAR(2)` · **Nullable:** no · **Indexed:** `users_country_idx`

**Definition.** Country the user signed up from, as ISO 3166-1 alpha-2 (e.g. `US`, `IN`, `DE`).

## Belongs to
[[users]]

## Lineage
- **Produced by:** signup form (geo-IP fallback if not provided).
- **Consumed by:** [[gmv|GMV]] reporting (segmented by country), tax/billing logic.

## Allowed values / domain
Uppercase ISO 3166-1 alpha-2. Not validated at DB level — relies on app enforcement.

## Notes
- Captures *signup* country; does not update on later moves. For current residence, use the (separate) `addresses` table.
