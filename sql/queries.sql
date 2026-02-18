-- =========================================================
-- Business Intelligence SQL Queries
-- Lab 3 - ETL & BI
-- These queries correspond to the business questions defined in the requirements.
-- =========================================================

-- ---------------------------------------------------------
-- Query 1: Sales Volume and Revenue by Product Category
-- ---------------------------------------------------------
-- Objective: Identify which product categories perform best in terms of
-- both volume (units sold) and total revenue generated.
SELECT p.category, 
       SUM(s.quantity) AS sales_volume, 
       SUM(s.total_amount) AS revenue
FROM sale s
JOIN product p ON s.product_idproduct = p.id_product
GROUP BY p.category
ORDER BY revenue DESC;

-- ---------------------------------------------------------
-- Query 2: Revenue by Sales Channel
-- ---------------------------------------------------------
-- Objective: Compare the performance of Physical Stores vs. Online Sales
-- to determine the most effective revenue stream.
SELECT c.channel, 
       SUM(s.total_amount) AS revenue
FROM sale s
JOIN channel c ON s.channel_idchannel = c.id_channel
GROUP BY c.channel
ORDER BY revenue DESC;

-- ---------------------------------------------------------
-- Query 3: Monthly Sales Trend (Revenue & Profit)
-- ---------------------------------------------------------
-- Objective: Analyze the evolution of sales over time to identify seasonal
-- patterns and compare gross revenue against net profit.
SELECT d.month, 
       SUM(s.total_amount) AS revenue,
       SUM(s.profit) AS profit
FROM sale s
JOIN date d ON s.date_iddate = d.id_date
GROUP BY d.month
ORDER BY d.month;

-- ---------------------------------------------------------
-- Query 4: Most Profitable Brands (Top 10)
-- ---------------------------------------------------------
-- Objective: Identify which brands generate the highest net profit.
-- This differs from revenue as it accounts for the cost of goods sold.
SELECT p.brand, 
       SUM(s.profit) AS total_profit
FROM sale s
JOIN product p ON s.product_idproduct = p.id_product
GROUP BY p.brand
ORDER BY total_profit DESC
LIMIT 10;
