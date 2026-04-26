---
type: pipeline
name: payments_reconciliation_dag
status: draft
owner: [[data-platform-team]]
sources: [raw/schemas/sample_ecommerce.sql, raw/pipelines/payments_reconciliation_dag.py]
source_hashes: {raw/schemas/sample_ecommerce.sql: b081203657f6072f, raw/pipelines/payments_reconciliation_dag.py: a63dd0e66daee51d}
tags: [airflow, scheduled, daily, finance]
last_updated: 2026-04-26
---

# payments_reconciliation_dag

**Daily Airflow DAG that rebuilds [[orders_daily|mart.orders_daily]] then reconciles captured [[payments]] against it.** Variance >1% per `(day, currency)` writes to an ops dashboard table; total daily variance >$5k pages oncall in `#data-platform` (per `raw/pipelines/payments_reconciliation_dag.py`).

**Schedule:** `0 6 * * *` (daily 06:00 UTC) · **Catchup:** off · **Retries:** 2, 10-minute delay · **SLA:** 3 hours (must complete by 09:00 UTC).

## Inputs
- [[orders]] (read indirectly via [[orders_daily_pipeline]] dbt run)
- [[payments]] — captured rows (`status='captured'`) with signed [[payments__amount_cents|amount_cents]]; refunds are negative amounts in the same column.

## Outputs
- [[orders_daily|mart.orders_daily]] — rebuilt by the first task.
- `mart.payments_variance_daily` — variance rows where `|orders_daily.gmv_gross_cents - sum(payments.amount_cents captured)| / orders_daily.gmv_gross_cents > 1%`. Not yet documented as a wiki page; tag `needs-info`.
- PagerDuty incident if absolute daily variance > $5,000 USD-equivalent.

## Tasks
| Task | Operator | Purpose |
| --- | --- | --- |
| `run_orders_daily` | `BashOperator` | `dbt run --select orders_daily` — rebuilds the mart. |
| `reconcile_payments` | `PythonOperator` | Sums captured [[payments__amount_cents]] per `(day, currency)`; compares to [[orders_daily__gmv_gross_cents|gmv_gross_cents]]; writes variance rows. |
| `emit_variance` | `PythonOperator` | Threshold check — pages oncall when daily variance > $5k. |

Sequence: `run_orders_daily >> reconcile_payments >> emit_variance`.

## Transformation
Reconciliation logic itself lives outside this repo (the Python callables are stubs that import from the data-platform repo). The DAG file in `raw/pipelines/` is the orchestration definition, not the business logic.

## Failure modes / SLAs
- **SLA breach (>3h):** routed via PagerDuty per `default_args.email_on_failure=False`.
- **Currency mismatch** between [[orders__currency|orders.currency]] and [[payments__currency|payments.currency]] for the same order surfaces as a variance row.
- **Refund timing:** refunds (negative [[payments__amount_cents]]) reduce net cash; gross GMV in [[orders_daily]] does not subtract them. Variance is expected to be non-zero — the threshold is what's monitored, not parity.

## Notes
- This DAG is the orchestrator for [[orders_daily_pipeline]]; the dbt model does not run on its own schedule.
- The stakeholders for the variance numbers differ — see [[gmv|GMV]] for the gross-vs-net-cash debate this DAG sits in the middle of.
