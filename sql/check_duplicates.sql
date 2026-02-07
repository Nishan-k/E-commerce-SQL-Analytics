-- @query: check_duplicates

WITH
	order_info AS (SELECT 
						o.order_id,  
						oi.price, oi.order_item_id,
						oi.freight_value, (oi.price + oi.freight_value) AS total
					FROM   
						order_items oi   LEFT JOIN  orders o
						ON  oi.order_id = o.order_id)
					
SELECT 
	order_id, order_item_id,
	COUNT(*) AS total
FROM 
	order_info 
GROUP BY 
	order_id, order_item_id
HAVING COUNT(*) > 1;