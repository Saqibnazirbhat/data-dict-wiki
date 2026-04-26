---
type: owner
name: Data Platform Team
status: draft
sources: [raw/schemas/sample_ecommerce.sql]
tags: [team]
last_updated: 2026-04-26
---

# Data Platform Team

**Charter.** Owns the warehouse, ingestion pipelines, and the canonical models that downstream teams depend on. Source of truth for schema definitions in `shop`.

## Owns
- **Tables:** [[users]], [[categories]], [[products]], [[orders]], [[order_items]], [[payments]]
- **Pipelines:** [[orders_daily_pipeline]], [[payments_reconciliation_dag]]
- **Concepts:** [[gmv|GMV]], [[order-lifecycle|order lifecycle]], [[revenue-recognition|revenue recognition]]

## Contact
Slack: `#data-platform`. Oncall rotation managed in PagerDuty.

## Notes
- Co-owns [[users]] with [[growth-team|Growth team]] — Growth owns the product surface, Data Platform owns the pipeline.
