
-- @query: customer_order_frequency_interpretation
WITH	customer_full_IDs AS (
								SELECT	coi.order_id, 
										coi.customer_id,
										c.customer_unique_id
								FROM	customer_order_info coi INNER JOIN customers c
											ON coi.customer_id = c.customer_id
							  ),
                                      
             
		orders_per_customer AS (
								SELECT	customer_unique_id,
                                        COUNT(DISTINCT order_id) AS total_orders
								FROM	customer_full_IDs
								GROUP BY	customer_unique_id
								)
                                
                                     
		 SELECT	customer_unique_id,
				total_orders,
				CASE 
					WHEN total_orders = 1 THEN 'One-Time Buyer'
					WHEN total_orders = 2 THEN 'Returning Customer'
					WHEN total_orders = 3 THEN 'Loyal Customer'
					WHEN total_orders = 4 THEN 'Very Loyal'
					ELSE 'VIP Customers'
				END AS Interpretation                   
		 FROM	orders_per_customer;