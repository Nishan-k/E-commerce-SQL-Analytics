-- @query: baseline_metrics
WITH	total_price_info AS 
							(SELECT	o.order_id,  oi.price, 
									oi.freight_value,
                                    o.order_status,
									(COALESCE(oi.price, 0) + COALESCE(oi.freight_value, 0)) AS total						
							 FROM	order_items oi   INNER JOIN  orders o
										ON  oi.order_id = o.order_id
							 WHERE	oi.price  IS NOT NULL AND oi.freight_value IS NOT NULL),
		
        baseline_metrics AS
							(SELECT	SUM(total) AS total_expected_revenue,
									SUM(CASE WHEN order_status = 'canceled' THEN total ELSE 0 END) AS total_cancelled_revenue_loss,
									SUM(CASE WHEN order_status = 'delivered' THEN total ELSE 0 END) AS total_revenue_from_delivered_items
							FROM	total_price_info),
                            
		baseline_metrics_pivoted AS (		
											SELECT	'Total Market Opportunity' AS Metrics, 
													 ROUND(total_expected_revenue / 1000000, 2) AS Amount_millions
											FROM	baseline_metrics

											UNION ALL
											SELECT 'Total Revenue Loss From Cancellation', 
													ROUND(total_cancelled_revenue_loss / 1000000, 2)
											FROM baseline_metrics

											UNION ALL
											SELECT 'Total Revenue Realized (Delivered Items)', 
													ROUND(total_revenue_from_delivered_items / 1000000, 2)
											FROM baseline_metrics)
		
        SELECT	*
        FROM baseline_metrics_pivoted;
            					
            
