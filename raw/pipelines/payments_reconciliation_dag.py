"""payments_reconciliation_dag

Daily orders rollup + payments reconciliation.

Sequence:
  1. run_orders_daily   — `dbt run --select orders_daily` (rebuilds mart.orders_daily)
  2. reconcile_payments — match payments.amount_cents (status='captured', signed)
                          against orders.total_cents per (order_day, currency)
  3. emit_variance      — write variance rows >1% to ops dashboard;
                          page #data-platform if total daily variance > $5k

Owner: data-platform-team
SLA:   complete by 09:00 UTC. Failure pages oncall in #data-platform.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

DEFAULT_ARGS = {
    "owner": "data-platform",
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
    "sla": timedelta(hours=3),
    "email_on_failure": False,  # routed via PagerDuty, not email
}


def reconcile_payments(**context) -> None:
    """Match payments to orders per (day, currency).

    Pulls captured payments (positive) and refunds (negative
    `amount_cents`) from `payments`, sums to net cash per day, and
    compares to mart.orders_daily.gmv_gross_cents. Variance rows go
    to the ops dashboard table `mart.payments_variance_daily`.
    """
    raise NotImplementedError("Reconciliation logic lives in the data-platform repo")


def emit_variance(**context) -> None:
    """Page oncall if absolute daily variance exceeds $5,000 USD-equivalent."""
    raise NotImplementedError("Variance threshold check lives in the data-platform repo")


with DAG(
    dag_id="payments_reconciliation_dag",
    description="Daily orders rollup + payments reconciliation against captured cash.",
    schedule="0 6 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=["payments", "orders", "daily", "finance"],
) as dag:

    run_orders_daily = BashOperator(
        task_id="run_orders_daily",
        bash_command="dbt run --select orders_daily",
    )

    reconcile = PythonOperator(
        task_id="reconcile_payments",
        python_callable=reconcile_payments,
    )

    variance = PythonOperator(
        task_id="emit_variance",
        python_callable=emit_variance,
    )

    run_orders_daily >> reconcile >> variance
