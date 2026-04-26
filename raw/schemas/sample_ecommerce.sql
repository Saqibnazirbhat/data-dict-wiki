-- ============================================================================
-- sample_ecommerce.sql
-- Production e-commerce OLTP schema (Postgres dialect).
-- Owner: data-platform-team. Source of truth for the `shop` schema in prod.
-- Touched by: orders_daily_pipeline (dbt), payments_reconciliation_dag (Airflow).
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS shop;

-- ----------------------------------------------------------------------------
-- users: every person who has ever signed up. Soft-delete via `status`.
-- PII: email, name. Do not export downstream without hashing.
-- Owned by: growth-team (product surface), data-platform-team (pipeline).
-- ----------------------------------------------------------------------------
CREATE TABLE shop.users (
    id            BIGSERIAL    PRIMARY KEY,
    email         TEXT         NOT NULL UNIQUE,        -- lowercase, validated at app layer
    name          TEXT         NOT NULL,
    country       CHAR(2)      NOT NULL,                -- ISO 3166-1 alpha-2
    status        TEXT         NOT NULL DEFAULT 'active',
                                                        -- enum: 'active' | 'suspended' | 'deleted'
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    deleted_at    TIMESTAMPTZ                          -- set when status='deleted' (GDPR)
);

CREATE INDEX users_country_idx ON shop.users (country);

-- ----------------------------------------------------------------------------
-- categories: product taxonomy. Self-referential (parent_id) for nesting.
-- ----------------------------------------------------------------------------
CREATE TABLE shop.categories (
    id          BIGSERIAL  PRIMARY KEY,
    name        TEXT       NOT NULL,
    parent_id   BIGINT     REFERENCES shop.categories(id),  -- NULL = top-level
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ----------------------------------------------------------------------------
-- products: catalog. price_cents stored as integer to avoid float math.
-- A product belongs to exactly one category. Soft-deleted via `status`.
-- ----------------------------------------------------------------------------
CREATE TABLE shop.products (
    id           BIGSERIAL    PRIMARY KEY,
    sku          TEXT         NOT NULL UNIQUE,           -- vendor-provided
    name         TEXT         NOT NULL,
    category_id  BIGINT       NOT NULL REFERENCES shop.categories(id),
    price_cents  INTEGER      NOT NULL CHECK (price_cents >= 0),
    currency     CHAR(3)      NOT NULL DEFAULT 'USD',    -- ISO 4217
    status       TEXT         NOT NULL DEFAULT 'active', -- 'active' | 'discontinued'
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX products_category_idx ON shop.products (category_id);

-- ----------------------------------------------------------------------------
-- orders: one row per customer order (the cart envelope, not the line items).
-- `total_cents` is denormalized — sum of line items at time of placement;
-- does NOT update if items are refunded later (see payments table for that).
-- ----------------------------------------------------------------------------
CREATE TABLE shop.orders (
    id            BIGSERIAL    PRIMARY KEY,
    user_id       BIGINT       NOT NULL REFERENCES shop.users(id),
    status        TEXT         NOT NULL DEFAULT 'pending',
                                                         -- 'pending' | 'paid' | 'shipped'
                                                         -- | 'delivered' | 'cancelled' | 'refunded'
    total_cents   BIGINT       NOT NULL CHECK (total_cents >= 0),
    currency      CHAR(3)      NOT NULL DEFAULT 'USD',
    placed_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
    shipped_at    TIMESTAMPTZ,                           -- NULL until shipment
    delivered_at  TIMESTAMPTZ                            -- NULL until carrier confirms
);

CREATE INDEX orders_user_idx        ON shop.orders (user_id);
CREATE INDEX orders_status_idx      ON shop.orders (status);
CREATE INDEX orders_placed_at_idx   ON shop.orders (placed_at);

-- ----------------------------------------------------------------------------
-- order_items: line items inside an order. Quantity * unit_price_cents
-- should reconcile to orders.total_cents at placement time (not after).
-- ----------------------------------------------------------------------------
CREATE TABLE shop.order_items (
    id                BIGSERIAL  PRIMARY KEY,
    order_id          BIGINT     NOT NULL REFERENCES shop.orders(id) ON DELETE CASCADE,
    product_id        BIGINT     NOT NULL REFERENCES shop.products(id),
    quantity          INTEGER    NOT NULL CHECK (quantity > 0),
    unit_price_cents  INTEGER    NOT NULL CHECK (unit_price_cents >= 0)
                                          -- snapshot of products.price_cents at order time
);

CREATE INDEX order_items_order_idx   ON shop.order_items (order_id);
CREATE INDEX order_items_product_idx ON shop.order_items (product_id);

-- ----------------------------------------------------------------------------
-- payments: every payment attempt against an order. An order can have many
-- payments (retries, partial captures, refunds-as-negative-amounts).
-- A payment is "real money moved" only when status = 'captured'.
-- PCI: do NOT store raw card data here — only the processor's token.
-- ----------------------------------------------------------------------------
CREATE TABLE shop.payments (
    id              BIGSERIAL    PRIMARY KEY,
    order_id        BIGINT       NOT NULL REFERENCES shop.orders(id),
    method          TEXT         NOT NULL,
                                                          -- 'card' | 'paypal' | 'apple_pay'
                                                          -- | 'gift_card' | 'bank_transfer'
    amount_cents    BIGINT       NOT NULL,                -- negative for refunds
    currency        CHAR(3)      NOT NULL DEFAULT 'USD',
    status          TEXT         NOT NULL,
                                                          -- 'authorized' | 'captured'
                                                          -- | 'failed' | 'refunded'
    processor_ref   TEXT         NOT NULL,                -- Stripe/Adyen txn id
    processed_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX payments_order_idx    ON shop.payments (order_id);
CREATE INDEX payments_status_idx   ON shop.payments (status);
