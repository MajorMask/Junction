-- Product table (from JSON, only basic fields for relational use)
CREATE TABLE products (
    product_code VARCHAR PRIMARY KEY,
    product_name VARCHAR,
    brand VARCHAR,
    category VARCHAR,
    country_of_origin VARCHAR
    -- Add more fields as needed from JSON
);

-- Sales Orders
CREATE TABLE sales_orders (
    order_number BIGINT,
    order_row_number INT,
    order_created_date DATE,
    order_created_time VARCHAR,
    requested_delivery_date DATE,
    customer_number BIGINT,
    product_code VARCHAR REFERENCES products(product_code),
    order_qty NUMERIC,
    sales_unit VARCHAR,
    delivery_number BIGINT,
    plant VARCHAR,
    storage_location VARCHAR,
    delivered_qty NUMERIC,
    transfer_number BIGINT,
    warehouse_number BIGINT,
    picking_confirmed_date DATE,
    picking_confirmed_time VARCHAR,
    picking_picked_qty NUMERIC,
    PRIMARY KEY (order_number, order_row_number)
);

-- Replacement Orders
CREATE TABLE replacement_orders (
    order_number BIGINT,
    order_row_number INT,
    order_created_date DATE,
    order_created_time VARCHAR,
    requested_delivery_date DATE,
    customer_number BIGINT,
    product_code VARCHAR REFERENCES products(product_code),
    order_qty NUMERIC,
    sales_unit VARCHAR,
    delivery_number BIGINT,
    plant VARCHAR,
    storage_location VARCHAR,
    delivered_qty NUMERIC,
    transfer_number BIGINT,
    warehouse_number BIGINT,
    picking_confirmed_date DATE,
    picking_confirmed_time VARCHAR,
    picking_picked_qty NUMERIC,
    PRIMARY KEY (order_number, order_row_number)
);

-- Purchase Orders
CREATE TABLE purchase_orders (
    order_number BIGINT,
    po_row_number INT,
    customer_number BIGINT,
    po_created_date DATE,
    requested_delivery_date DATE,
    product_code VARCHAR REFERENCES products(product_code),
    plant VARCHAR,
    storage_location VARCHAR,
    ordered_qty NUMERIC,
    unit VARCHAR,
    received_qty NUMERIC,
    PRIMARY KEY (order_number, po_row_number)
);

-- Indexes for fast lookup
CREATE INDEX idx_sales_product ON sales_orders(product_code);
CREATE INDEX idx_replacement_product ON replacement_orders(product_code);
CREATE INDEX idx_purchase_product ON purchase_orders(product_code);

CREATE INDEX idx_sales_customer ON sales_orders(customer_number);
CREATE INDEX idx_replacement_customer ON replacement_orders(customer_number);
CREATE INDEX idx_purchase_customer ON purchase_orders(customer_number);

-- Example: Query to find buffer margin and confidence score (pseudo-SQL)
-- SELECT product_code, SUM(order_qty) AS total_ordered, SUM(delivered_qty) AS total_delivered, SUM(received_qty) AS total_received
-- FROM sales_orders
-- JOIN purchase_orders USING (product_code)
-- GROUP BY product_code;
