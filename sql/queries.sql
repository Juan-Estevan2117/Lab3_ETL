-- 1. Volumen de ventas e ingresos por categoría de producto 
SELECT p.category, 
       SUM(s.quantity) AS sales_volume, 
       SUM(s.quantity * s.unit_price_sale) AS total_revenue
FROM sale s
JOIN product p ON s.product_idproduct = p.id_product
GROUP BY p.category;

-- 2. Canales de venta que generan mayores ingresos 
SELECT c.channel, 
       SUM(s.quantity * s.unit_price_sale) AS total_revenue
FROM sale s
JOIN channel c ON s.channel_idchannel = c.id_channel
GROUP BY c.channel
ORDER BY total_revenue DESC;

-- 3. Evolución de ventas en el tiempo (tendencia mensual) 
SELECT d.year, d.month, 
       SUM(s.quantity * s.unit_price_sale) AS total_revenue
FROM sale s
JOIN date d ON s.date_iddate = d.id_date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 4. Marcas más rentables (Ganancia = Ingresos - Costos) 
SELECT p.brand, 
       SUM(s.quantity * (s.unit_price_sale - p.unit_cost)) AS total_profit
FROM sale s
JOIN product p ON s.product_idproduct = p.id_product
GROUP BY p.brand
ORDER BY total_profit DESC;