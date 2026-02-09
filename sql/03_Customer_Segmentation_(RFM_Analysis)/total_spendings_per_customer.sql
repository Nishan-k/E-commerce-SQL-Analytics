-- @query: total_spendings_per_customer
WITH	order_info AS (
						SELECT	oi.order_id,
								(oi.price + oi.freight_value) AS total_amount,
								o.customer_id
                        FROM	order_items oi INNER JOIN orders o
									ON oi.order_id = o.order_id
                        WHERE	o.order_status = 'delivered')
                            
                            
         SELECT	c.customer_unique_id,
				SUM(o_info.total_amount) AS total_amount
         FROM	order_info o_info INNER JOIN customers c
					ON o_info.customer_id = c.customer_id
         GROUP BY	c.customer_unique_id
         ORDER BY	SUM(o_info.total_amount) DESC;