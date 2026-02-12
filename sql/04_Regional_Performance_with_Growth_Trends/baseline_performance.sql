-- @query: highest_revenue_by_state_w_customer_info


WITH	order_info_cte AS 
							(SELECT  oi.order_id, oi.order_item_id, 
									oi.price + oi.freight_value AS total_amount,
									o.customer_id, o.order_status
							FROM    order_items oi INNER JOIN orders o
									ON oi.order_id = o.order_id
							WHERE   o.order_status = 'delivered'),
                        
            
		customer_full_info_cte AS 
									(SELECT	oic.order_id, oic.order_item_id, 
											oic.total_amount, oic.customer_id,
											c.customer_unique_id, c.customer_zip_code_prefix,
											c.customer_city, c.customer_state
									FROM 	order_info_cte oic LEFT JOIN customers c
											ON oic.customer_id = c.customer_id),
                    
                    
            
		customer_spendings_w_geo_info_cte AS 
											  (SELECT	customer_unique_id,
														SUM(total_amount) AS total_spending,
														MAX(customer_zip_code_prefix) AS zip_code,
														MAX(customer_city) AS city,
														MAX(customer_state) AS state
											  FROM 		customer_full_info_cte
											  GROUP BY customer_unique_id)
                          
            
           SELECT	* 
           FROM		customer_spendings_w_geo_info_cte;
           
           
           
           
-- @query: highest_volume_of_orders_by_state
WITH	order_info_cte AS 
							(SELECT  oi.order_id, oi.order_item_id, 
									oi.price + oi.freight_value AS total_amount,
									o.customer_id, o.order_status
							FROM    order_items oi INNER JOIN orders o
									ON oi.order_id = o.order_id
							WHERE   o.order_status = 'delivered'),
                        
            
		customer_full_info_cte AS 
									(SELECT	oic.order_id, oic.order_item_id, 
											oic.total_amount, oic.customer_id,
											c.customer_unique_id, c.customer_zip_code_prefix,
											c.customer_city, c.customer_state
									FROM 	order_info_cte oic LEFT JOIN customers c
											ON oic.customer_id = c.customer_id),
		
        order_count_per_customer AS 
									(
                                    SELECT	customer_unique_id,
											COUNT(DISTINCT order_id) AS total_orders
									FROM	customer_full_info_cte
									GROUP BY customer_unique_id
                                    )
                                    
		SELECT	opc.customer_unique_id, 
				opc.total_orders,
				c.customer_state
		FROM	order_count_per_customer opc INNER JOIN	customers c
				ON	opc.customer_unique_id = c.customer_unique_id;
                                            
		