---
type: column
name: users.status
status: draft
owner: [[growth-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [stable]
last_updated: 2026-04-26
---

# users.status

**Type:** `TEXT` · **Nullable:** no · **Default:** `'active'`

**Definition.** Lifecycle state of the user account. Owned semantically by [[growth-team|Growth team]].

## Belongs to
[[users]]

## Lineage
- **Produced by:** signup (defaults to `active`); admin actions; GDPR delete flow.

## Allowed values / domain
- `active` — normal user, can log in and transact.
- `suspended` — temporarily blocked (fraud, abuse). Login disabled; data retained.
- `deleted` — GDPR delete. Login disabled; [[users__deleted_at|deleted_at]] is set; PII fields scrubbed by a separate job.

## Notes
- Not enforced as a DB enum — application-validated only.
- Most analytics should filter `WHERE status = 'active'` AND `deleted_at IS NULL`.
