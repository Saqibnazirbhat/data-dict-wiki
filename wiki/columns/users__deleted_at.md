---
type: column
name: users.deleted_at
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [stable]
last_updated: 2026-04-26
---

# users.deleted_at

**Type:** `TIMESTAMPTZ` · **Nullable:** yes · **Default:** NULL

**Definition.** Timestamp at which the user requested account deletion (GDPR). Set together with [[users__status|status]] = `'deleted'`.

## Belongs to
[[users]]

## Lineage
- **Produced by:** GDPR delete flow (admin job or self-service).

## Notes
- Most active-user queries should filter `WHERE deleted_at IS NULL`.
- A separate background job scrubs PII columns ([[users__email|email]], [[users__name|name]]) some time after this is set; the row itself is retained for referential integrity with [[orders]].
