-- 1. Sales volume and revenue per product category
SELECT p.category, 
       SUM(s.quantity) AS sales_volume, 
       SUM(s.total_amount) AS revenue
FROM sale s
JOIN product p ON s.product_idproduct = p.id_product
GROUP BY p.category
ORDER BY revenue DESC;

-- 2. Sales channels by revenue
SELECT c.channel, 
       SUM(s.total_amount) AS revenue
FROM sale s
JOIN channel c ON s.channel_idchannel = c.id_channel
GROUP BY c.channel
ORDER BY revenue DESC;

-- 3. Sales evolution over time (monthly trend)
SELECT d.month, 
       SUM(s.total_amount) AS revenue,
       SUM(s.profit) AS profit
FROM sale s
JOIN date d ON s.date_iddate = d.id_date
GROUP BY d.month
ORDER BY d.month;

-- 4. Most profitable brands (Requirement 4 of the Lab)
SELECT p.brand, 
       SUM(s.profit) AS total_profit
FROM sale s
JOIN product p ON s.product_idproduct = p.id_product
GROUP BY p.brand
ORDER BY total_profit DESC
LIMIT 10;
