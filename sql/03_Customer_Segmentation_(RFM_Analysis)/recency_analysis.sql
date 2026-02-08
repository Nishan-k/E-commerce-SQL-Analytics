-- @query: recency_analysis
WITH	customer_order_window AS 
							(SELECT	customer_id, 
									order_purchase_timestamp,
									ROW_NUMBER() OVER(PARTITION BY customer_ID ORDER BY order_purchase_timestamp DESC) AS test
							FROM	customer_order_info),
                               
                                        
		data_threshold AS 
							(SELECT	DATE(MAX(order_purchase_timestamp), '+10 days') AS date_threshold
							 FROM	customer_order_info),
                           
                               
		recency_table AS 
						(SELECT		cow.customer_id,
									DATE(cow.order_purchase_timestamp) AS latest_purchase_timestamp,
									dt.date_threshold AS date_threshold,
									CAST(JULIANDAY(dt.date_threshold) - JULIANDAY(cow.order_purchase_timestamp) AS INTEGER) AS days_since_last_purchase
						FROM		customer_order_window cow CROSS JOIN data_threshold dt
						WHERE		test = 1)
        
        
		SELECT	customer_id,
                latest_purchase_timestamp,
                date_threshold,
                days_since_last_purchase,
                CAST((days_since_last_purchase / 50) * 10 AS INTEGER) AS bins
		FROM recency_table;