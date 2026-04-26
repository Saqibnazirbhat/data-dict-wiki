---
type: column
name: users.name
status: draft
owner: [[growth-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [pii, stable]
last_updated: 2026-04-26
---

# users.name

**Type:** `TEXT` · **Nullable:** no

**Definition.** The user's display name as entered at signup. Free-form, not validated for structure (single field — not split into first/last).

## Belongs to
[[users]]

## Lineage
- **Produced by:** signup form / profile edit.

## Allowed values / domain
Any non-empty string. No length cap at DB level (app limits to 200 chars).

## Notes
- **PII.** Mask in any analytical export.
