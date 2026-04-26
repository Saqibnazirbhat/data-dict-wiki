---
type: pipeline
name: payments_reconciliation_dag
status: stub
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f}
tags: [airflow, scheduled, finance]
last_updated: 2026-04-26
---

# payments_reconciliation_dag

**Nightly Airflow DAG that reconciles our [[payments]] table against the upstream processor's settlement export.** Referenced in the source schema header; DAG file not yet ingested.

## Inputs (presumed)
- [[payments]]
- Processor settlement file (Stripe / Adyen export — to be ingested as `raw/pipelines/...`)

## Outputs (presumed)
- A reconciliation report; data-quality alerts (e.g. currency mismatch between [[orders__currency|orders.currency]] and [[payments__currency|payments.currency]] for the same order).

## Stub — needs ingest of:
- The Airflow DAG file (drop into `raw/pipelines/`)
- Settlement file format / schema

Tagged `needs-info` until then.
