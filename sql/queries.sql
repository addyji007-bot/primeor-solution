
-- 1. Top 10 profitable products
SELECT
    product_name,
    ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY product_name
ORDER BY total_profit DESC
LIMIT 10;


-- 2. Top 10 customers by sales
SELECT
    customer_name,
    ROUND(SUM(sales), 2) AS total_sales
FROM orders
WHERE customer_name <> 'Unknown Customer'
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 10;


-- 3. Region-wise total sales
SELECT
    region,
    ROUND(SUM(sales), 2) AS total_sales
FROM orders
GROUP BY region
ORDER BY total_sales DESC;


-- 4. Category-wise average profit
SELECT
    category,
    ROUND(AVG(profit), 2) AS avg_profit
FROM orders
GROUP BY category
ORDER BY avg_profit DESC;


-- 5. Highest discount category (by average discount)
SELECT
    category,
    ROUND(AVG(discount), 3) AS avg_discount
FROM orders
GROUP BY category
ORDER BY avg_discount DESC
LIMIT 1;


-- 6. Orders with negative profit
SELECT
    order_id,
    product_name,
    category,
    sales,
    profit,
    discount
FROM orders
WHERE profit < 0
ORDER BY profit ASC;


-- 7. Monthly sales trend
SELECT
    year_month,
    ROUND(SUM(sales), 2) AS total_sales
FROM orders
GROUP BY year_month
ORDER BY year_month;


-- 8. Market-wise revenue analysis
SELECT
    market,
    ROUND(SUM(sales), 2)  AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(profit_margin), 2) AS avg_margin_pct
FROM orders
GROUP BY market
ORDER BY total_sales DESC;


-- 9. Top-performing sub-categories (by profit)
SELECT
    sub_category,
    ROUND(SUM(sales), 2)  AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY sub_category
ORDER BY total_profit DESC
LIMIT 10;


-- 10. Ship mode usage analysis
SELECT
    ship_mode,
    COUNT(*)                      AS order_count,
    ROUND(AVG(shipping_days), 2)  AS avg_shipping_days,
    ROUND(SUM(sales), 2)          AS total_sales
FROM orders
GROUP BY ship_mode
ORDER BY order_count DESC;

-- 11. Year-over-year sales growth
SELECT
    year,
    total_sales,
    ROUND(
        (total_sales - LAG(total_sales) OVER (ORDER BY year))
        / LAG(total_sales) OVER (ORDER BY year) * 100
    , 2) AS yoy_growth_pct
FROM (
    SELECT year, SUM(sales) AS total_sales
    FROM orders
    GROUP BY year
) AS yearly
ORDER BY year;


-- 12. Running total of sales by month
SELECT
    year_month,
    monthly_sales,
    ROUND(SUM(monthly_sales) OVER (ORDER BY year_month), 2) AS cumulative_sales
FROM (
    SELECT year_month, SUM(sales) AS monthly_sales
    FROM orders
    GROUP BY year_month
) AS monthly
ORDER BY year_month;


-- 13. Customer purchase frequency (basic RFM building block)
SELECT
    customer_name,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(sales), 2)     AS total_spend,
    ROUND(AVG(sales), 2)     AS avg_order_value
FROM orders
WHERE customer_name <> 'Unknown Customer'
GROUP BY customer_name
ORDER BY total_spend DESC
LIMIT 20;


-- 14. Products that are heavily discounted AND loss-making
SELECT
    product_name,
    sub_category,
    ROUND(AVG(discount), 2) AS avg_discount,
    ROUND(SUM(profit), 2)   AS total_profit,
    COUNT(*)                 AS order_count
FROM orders
WHERE discount >= 0.30
GROUP BY product_name, sub_category
HAVING SUM(profit) < 0
ORDER BY total_profit ASC
LIMIT 15;


-- 15. Rank sub-categories within each category by profit
SELECT
    category,
    sub_category,
    total_profit,
    RANK() OVER (
        PARTITION BY category ORDER BY total_profit DESC
    ) AS profit_rank_in_category
FROM (
    SELECT category, sub_category, SUM(profit) AS total_profit
    FROM orders
    GROUP BY category, sub_category
) AS subcat_profit
ORDER BY category, profit_rank_in_category;


-- 16. Segment x Region sales matrix
SELECT
    segment,
    region,
    ROUND(SUM(sales), 2) AS total_sales
FROM orders
GROUP BY segment, region
ORDER BY segment, total_sales DESC;


-- 17. Average shipping days by region AND ship mode combined
SELECT
    region,
    ship_mode,
    ROUND(AVG(shipping_days), 2) AS avg_shipping_days,
    COUNT(*) AS order_count
FROM orders
GROUP BY region, ship_mode
ORDER BY region, avg_shipping_days DESC;


-- 18. Quarterly profit margin trend
SELECT
    year,
    quarter,
    ROUND(AVG(profit_margin), 2) AS avg_profit_margin_pct
FROM orders
GROUP BY year, quarter
ORDER BY year, quarter;
