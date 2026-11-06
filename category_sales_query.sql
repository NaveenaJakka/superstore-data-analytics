-- 1. Category sales and profit
SELECT
    p.category AS category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND(SUM(f.profit) * 100.0 / NULLIF(SUM(f.sales), 0), 2) AS profit_margin_pct
FROM fact_sales AS f
INNER JOIN dim_product AS p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sales DESC;


-- 2. Monthly sales trend
SELECT
    substr(f.order_date, 1, 7) AS year_month,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit
FROM fact_sales AS f
GROUP BY substr(f.order_date, 1, 7)
ORDER BY year_month;


-- 3. Top 10 customers by sales
SELECT
    c.customer_name,
    c.segment,
    c.state,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    COUNT(DISTINCT f.order_id) AS order_count
FROM fact_sales AS f
INNER JOIN dim_customer AS c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.segment, c.state
ORDER BY total_sales DESC
LIMIT 10;


-- 4. Top 10 products by profit
SELECT
    p.product_name,
    p.category,
    p.sub_category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    SUM(f.quantity) AS units_sold
FROM fact_sales AS f
INNER JOIN dim_product AS p ON f.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category, p.sub_category
ORDER BY total_profit DESC
LIMIT 10;


-- 5. Most loss-making products
SELECT
    p.product_name,
    p.category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    SUM(f.quantity) AS units_sold
FROM fact_sales AS f
INNER JOIN dim_product AS p ON f.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
HAVING SUM(f.profit) < 0
ORDER BY total_profit ASC
LIMIT 10;


-- 6. Sales and profit by customer segment
SELECT
    c.segment,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND(SUM(f.profit) * 100.0 / NULLIF(SUM(f.sales), 0), 2) AS profit_margin_pct,
    COUNT(DISTINCT c.customer_id) AS customers
FROM fact_sales AS f
INNER JOIN dim_customer AS c ON f.customer_id = c.customer_id
GROUP BY c.segment
ORDER BY total_sales DESC;


-- 7. Shipping mode performance
SELECT
    f.ship_mode,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    COUNT(DISTINCT f.order_id) AS order_count,
    ROUND(AVG(julianday(f.ship_date) - julianday(f.order_date)), 1) AS avg_ship_days
FROM fact_sales AS f
GROUP BY f.ship_mode
ORDER BY total_sales DESC;


-- 8. Discount impact on sales and profitability
SELECT
    CASE
        WHEN discount = 0 THEN '0% Discount'
        WHEN discount <= 0.20 THEN '1%-20% Discount'
        WHEN discount <= 0.40 THEN '21%-40% Discount'
        ELSE 'Above 40% Discount'
    END AS discount_band,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(discount) * 100, 1) AS average_discount_pct,
    COUNT(*) AS sales_records
FROM fact_sales
GROUP BY discount_band
ORDER BY MIN(discount);
