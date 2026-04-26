---
type: pipeline
name: orders_daily_pipeline
status: stub
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
tags: [dbt, scheduled]
last_updated: 2026-04-26
---

# orders_daily_pipeline

**Daily aggregation of [[orders]] + [[order_items]] into a `mart.orders_daily` table for BI.** Referenced in the source schema header but the pipeline definition itself is not yet ingested.

## Inputs (presumed)
- [[orders]], [[order_items]], [[users]], [[products]], [[categories]]

## Outputs (presumed)
- `mart.orders_daily` (not yet documented as a wiki page)

## Stub — needs ingest of:
- The dbt model SQL (drop into `raw/pipelines/`)
- Schedule / orchestration config

Tagged `needs-info` until then.
