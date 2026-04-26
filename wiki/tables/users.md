---
type: table
name: users
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [pii, growth, stable]
last_updated: 2026-04-26
---

# users

**Every person who has ever signed up.** Soft-deleted via `status='deleted'` (GDPR — `deleted_at` is set, row is retained). Contains [[#Notes|PII]]: do not export downstream without hashing.

## Grain
One row per registered user. Natural key: `email` (UNIQUE). Surrogate key: `id`.

## Columns
| Column | Type | Description |
| --- | --- | --- |
| [[users__id\|id]] | `BIGSERIAL` PK | Surrogate user id. |
| [[users__email\|email]] | `TEXT` UNIQUE | Lowercase, validated at app layer. PII. |
| [[users__name\|name]] | `TEXT` | Full display name. PII. |
| [[users__country\|country]] | `CHAR(2)` | ISO 3166-1 alpha-2 country code. |
| [[users__status\|status]] | `TEXT` | Lifecycle: `active` / `suspended` / `deleted`. |
| [[users__created_at\|created_at]] | `TIMESTAMPTZ` | Signup timestamp. |
| [[users__deleted_at\|deleted_at]] | `TIMESTAMPTZ` NULL | Set when `status='deleted'`. |

## Upstream
- Application writes (signup flow, admin panel).
- Source DDL: `raw/schemas/sample_ecommerce.sql`.

## Downstream
- [[orders]] references `users.id` via `orders.user_id`.
- [[orders_daily_pipeline]] joins this table to compute per-user metrics.
- Powers [[gmv|GMV]] reporting (segmented by [[users__country|country]]).

## Notes
- **PII.** `email` and `name` are personal data. The standard masked view `mart.users_safe` should be used downstream.
- **Soft-delete.** Rows with `status='deleted'` remain in the table; filter on `deleted_at IS NULL` for active-user analytics.
- Co-owned: [[growth-team|Growth team]] owns the product surface and the `status` enum semantics; [[data-platform-team|Data Platform]] owns the pipeline. (per `raw/schemas/sample_ecommerce.sql` header)
