-- @query: drop_customer_order_table_if_exists
DROP	TABLE IF EXISTS	customer_order_info;



-- @query: create_temp_table
CREATE TEMP TABLE customer_order_info  AS 
                SELECT
                    oi.order_id, oi.order_item_id, oi.price, oi.freight_value,
                    oi.product_id,
                    o.customer_id, o.order_status, o.order_purchase_timestamp
                FROM
                    order_items oi INNER JOIN orders o
                        ON oi.order_id = o.order_id
                WHERE
                    o.order_status = 'delivered';
                    
                    