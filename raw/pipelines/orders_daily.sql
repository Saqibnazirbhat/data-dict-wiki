{{ config(
    materialized='table',
    schema='mart',
    tags=['daily', 'orders', 'core']
) }}

-- models/marts/orders_daily.sql
--
-- Daily order rollup. One row per (order_day, currency).
-- Owner: data-platform-team. Schedule: 06:00 UTC daily via Airflow
-- DAG `payments_reconciliation_dag`.
--
-- Refunds are NOT subtracted here — this is the gross GMV variant
-- (see wiki concept `gmv`). For net cash, aggregate `payments` instead.

with orders_filtered as (
    select
        date_trunc('day', placed_at)::date as order_day,
        currency,
        status,
        total_cents
    from {{ ref('stg_orders') }}
    where status in ('paid', 'shipped', 'delivered')
)

select
    order_day,
    currency,
    sum(case when status = 'paid'      then 1 else 0 end) as orders_paid,
    sum(case when status = 'shipped'   then 1 else 0 end) as orders_shipped,
    sum(case when status = 'delivered' then 1 else 0 end) as orders_delivered,
    count(*)                                              as orders_total,
    sum(total_cents)                                      as gmv_gross_cents
from orders_filtered
group by 1, 2
