-- ##################################
-- Break down of the orders based on their order_status:
-- ##################################

-- @query: breakdown_by_order_status
SELECT	order_status,
		COUNT(*) AS total_n_orders
FROM	orders
GROUP BY order_status
ORDER BY total_n_orders DESC;     
   

-- ##################################
-- Break down on cancelled orders:
-- ##################################

-- @query: without_items
SELECT	COUNT(*) AS canceled_orders_without_items
FROM	orders o
		LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE	o.order_status = 'canceled'
		AND oi.order_id IS NULL;
        
        
-- @query: with_items
SELECT	COUNT(DISTINCT o.order_id) AS canceled_orders_with_items
FROM 	orders o
		JOIN order_items oi
			ON o.order_id = oi.order_id
WHERE	o.order_status = 'canceled'
		AND 
        oi.order_id IS NOT NULL;