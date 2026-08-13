
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    order_id        VARCHAR(50),
    order_date      DATE,
    ship_date       DATE,
    ship_mode       VARCHAR(50),
    customer_name   VARCHAR(150),
    segment         VARCHAR(50),
    state           VARCHAR(100),
    country         VARCHAR(100),
    market          VARCHAR(50),
    region          VARCHAR(50),
    product_id      VARCHAR(50),
    category        VARCHAR(50),
    sub_category    VARCHAR(50),
    product_name    VARCHAR(255),
    sales            DECIMAL(12,2),
    quantity        INT,
    discount        DECIMAL(5,3),
    profit          DECIMAL(12,4),
    shipping_cost   DECIMAL(10,2),
    order_priority  VARCHAR(20),
    year            INT,
    profit_estimated  TINYINT(1),
    shipping_days   INT,
    profit_margin   DECIMAL(10,4),
    `year_month`      VARCHAR(7),
    quarter         VARCHAR(2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Indexes on columns used often in WHERE / GROUP BY / JOIN,
-- since this table will be queried a lot for the tasks below.
CREATE INDEX idx_orders_region       ON orders(region);
CREATE INDEX idx_orders_category     ON orders(category);
CREATE INDEX idx_orders_order_date   ON orders(order_date);
CREATE INDEX idx_orders_year_month   ON orders(`year_month`);
CREATE INDEX idx_orders_customer     ON orders(customer_name(100));
