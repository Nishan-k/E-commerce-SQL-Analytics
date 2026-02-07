-- @query: cncl_per_prod_category_amount

WITH	order_prod_info_table AS (                   
                                    SELECT
                                       o.order_id, oi.order_item_id, 
                                       p.product_category_name,
                                       o.order_status,
                                       p.product_id,
                                       oi.price, oi.freight_value,
                                       (oi.price + oi.freight_value) AS total_amount
                                    FROM
                                        order_items oi LEFT JOIN orders o
                                            ON oi.order_id = o.order_id
                                        LEFT JOIN products p 
                                            ON oi.product_id = p.product_id
                                    WHERE
                                        o.order_status = 'canceled'
                                    ),
                                        
                                
       
           orders_cncl_w_prod_cat_name AS ( 
                                        SELECT
                                           product_category_name_english, total_amount,
                                           order_status
                                        FROM
                                            order_prod_info_table AS opinf 
                                            LEFT JOIN product_category_translation AS pct
                                                ON opinf.product_category_name = pct.product_category_name
                                            ),
                                                
                                                
           lost_amount_per_category AS (
                                       SELECT
                                            COALESCE(product_category_name_english, 'Unknown') AS product_category,
                                            SUM(total_amount) AS total_amount
                                       FROM 
                                            orders_cncl_w_prod_cat_name
                                       GROUP BY
                                            product_category_name_english
                                        )

        SELECT	product_category,
				total_amount,
				ROUND((total_amount / (SELECT SUM(total_amount) FROM lost_amount_per_category)) * 100, 3) AS revenue_leak_percentage
        FROM    lost_amount_per_category
        ORDER BY	total_amount DESC;       