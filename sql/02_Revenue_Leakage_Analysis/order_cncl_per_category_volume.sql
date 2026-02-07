-- @query: cncl_per_prod_category_volume
WITH	order_prod_info_table AS (
								  SELECT	o.order_id, oi.order_item_id, 
											p.product_category_name,
                                            o.order_status,
                                            p.product_id,
                                            oi.price, oi.freight_value,
                                            (oi.price + oi.freight_value) AS total_amount
									FROM	order_items oi LEFT JOIN orders o
												ON oi.order_id = o.order_id
											LEFT JOIN products p 
												ON oi.product_id = p.product_id
                                    WHERE	o.order_status = 'canceled'
                                            ),             
                                                      
                                            
                              
                                
            orders_cncl_w_prod_cat_name AS ( 
										  SELECT	order_id, order_item_id,
													COALESCE(product_category_name_english, 'Unknown') AS product_category, 
													total_amount,
													order_status
										  FROM		order_prod_info_table AS opinf 
													LEFT JOIN product_category_translation AS pct
														ON opinf.product_category_name = pct.product_category_name
										)
                                            
           SELECT	product_category,
					COUNT(order_id) AS total_n_orders
           FROM     orders_cncl_w_prod_cat_name
           GROUP BY	product_category
           ORDER BY	total_n_orders DESC;