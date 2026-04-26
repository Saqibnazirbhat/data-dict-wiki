---
type: pipeline
name: stg_orders
status: stub
owner: [[data-platform-team]]
sources: [raw/pipelines/orders_daily.sql]
source_hashes: {raw/pipelines/orders_daily.sql: 319b2b89c80ee01f}
tags: [dbt, staging, needs-info]
last_updated: 2026-04-26
---

# stg_orders

**dbt staging model that wraps the raw [[orders]] table.** Referenced by [[orders_daily_pipeline]] via `{{ ref('stg_orders') }}` but its own SQL has not yet been ingested.

## Stub — needs ingest of:
- The staging model SQL (drop into `raw/pipelines/`).
- Schema/column transforms applied at the staging layer (renames, type casts, soft-delete filters, etc.).

Tagged `needs-info` until then.
