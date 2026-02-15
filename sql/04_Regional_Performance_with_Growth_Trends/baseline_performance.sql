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
											COUNT(DISTINCT order_id) AS total_orders,
                                            MAX(customer_state) AS state
									FROM	customer_full_info_cte
									GROUP BY customer_unique_id
                                    )
                                    
		
        SELECT * FROM order_count_per_customer;
                                    


-- @query: orders_and_revenue_by_time_period_per_state

WITH	ord_lvl_info AS 
					(SELECT	o.customer_id,
                            oi.order_id, oi.order_item_id, o.order_purchase_timestamp,
                            oi.price, 
                            oi.freight_value
                    FROM  	order_items oi INNER JOIN orders o
                            ON oi.order_id = o.order_id
                    WHERE 	o.order_status = 'delivered'),
                    
    
		cust_ord_info AS 
						(SELECT	c.customer_unique_id, 
								oi.order_id, 
								oi.order_item_id, 
								STRFTIME("%Y-%m", oi.order_purchase_timestamp) as time_period, 
								(oi.price + oi.freight_value) AS total_amount,
								c.customer_state AS state
						FROM 	ord_lvl_info oi LEFT JOIN customers c
								ON oi.customer_id = c.customer_id)
    

        SELECT	time_period,
				state,
				COUNT(order_item_id) AS total_orders,
				SUM(total_amount) as total_revenue
        FROM 	cust_ord_info
        GROUP BY time_period, state;



                                            
		