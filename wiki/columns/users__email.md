---
type: column
name: users.email
status: draft
owner: [[growth-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [pii, stable]
last_updated: 2026-04-26
---

# users.email

**Type:** `TEXT` · **Nullable:** no · **UNIQUE**

**Definition.** The user's email address. The natural key for [[users]] and the login identifier.

## Belongs to
[[users]]

## Lineage
- **Produced by:** signup form (validated and lowercased at the app layer).
- **Consumed by:** marketing systems (via a separately-hashed export — never raw).

## Allowed values / domain
Lowercase RFC-5322 email; uniqueness enforced at DB level.

## Notes
- **PII.** Do not export raw downstream — use the `mart.users_safe` masked view.
