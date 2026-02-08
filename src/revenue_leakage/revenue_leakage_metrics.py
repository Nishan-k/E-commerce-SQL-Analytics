import pandas as pd
from pathlib import Path
from utils.helper import execute_query



# --------------------------------
# Revenue Leakage Specific Wrappers:
# --------------------------------


# -----------------------------------------------------------------------------------
# 1. Get the baseline metrics:
# -----------------------------------------------------------------------------------

def get_baseline_metrics(conn, sql_base_path:Path) -> pd.DataFrame:
    """
    This function will be responsible to calculate the baseline revenue metrics.

    Returns:
    --------
    pd.Dataframe with the baseline metrics
    """
    return execute_query(conn=conn,
                         sql_path = sql_base_path / "baseline_revenue_metrics.sql",
                         query_name="baseline_metrics", expected_columns=['Metrics', 'Amount_millions'])



# -----------------------------------------------------------------------------------
# 2. Calculate the revenue leakage percentage:
# -----------------------------------------------------------------------------------

def generate_revenue_leakage(revenue_baseline_metrics):
    """
    A function that calculates the revenue leakage:
    
    Parameters:
    -----------
    revenue_baseline_metrics: A revenue metrics dataframe
    """
    metrics_dict = revenue_baseline_metrics.set_index('Metrics')['Amount_millions'].to_dict()
    total_expected_revenue = metrics_dict['Total Market Opportunity']
    total_cancelled_revenue = metrics_dict['Total Revenue Loss From Cancellation']
    revenue_leakage_percentage = (total_cancelled_revenue / total_expected_revenue) * 100
    
    
    return revenue_leakage_percentage


# -----------------------------------------------------------------------------------
# 3. The breakdown of order counts by order status:
# -----------------------------------------------------------------------------------

def get_breakdown_of_orders(conn, sql_base_path:Path) -> pd.DataFrame:
    """
    This function will be responsible to handle queries related to `Order Status Breakdown`

    Returns:
    --------
    pd.Dataframe with the columns:
    1. order_status
    2. total_n_orders
    """

    return execute_query(conn=conn, sql_path=sql_base_path / "breakdown_of_orders.sql", 
                         query_name='breakdown_by_order_status', expected_columns=['order_status', 'total_n_orders'])

    


# -----------------------------------------------------------------------------------
# 4. Break down on canceled orders:
# -----------------------------------------------------------------------------------

def get_break_down_on_cncl_orders(conn, sql_base_path:Path) -> dict[str, pd.DataFrame]:
    """
    This function will be responsible to drill down the amount lost and 
    their contribution in the total revenue leakage due to order cancelation per category
    

    Returns:
    --------
    a dictionary with key as query_name and value as pd.Dataframe which has columns:
    product_category: Contains the product category names
    total_amount: Amount lost due to order cancelation
    revenue_leak_percentage: Contribution to the total revenue leakage in %
    
    """

    return {
       "without_items": execute_query(conn=conn, 
                                      sql_path=sql_base_path / "breakdown_of_orders.sql", 
                                      query_name="without_items",
                                      expected_columns=['canceled_orders_without_items']),
        
        "with_items": execute_query(conn=conn, 
                                    sql_path=sql_base_path / "breakdown_of_orders.sql", 
                                    query_name="with_items",
                                    expected_columns=['canceled_orders_with_items'])
            }


# -----------------------------------------------------------------------------------
# 5. Break down on canceled product category by total amount and their contribution to the revenue leakage:
# -----------------------------------------------------------------------------------

def get_cncl_by_prod_cat_amount(conn, sql_base_path:Path) -> pd.DataFrame:
    """
    This function will be responsible to return the product categories that were canceled, the amount lost and the revenue leakage in %.

    Returns:
    --------
    pd.Dataframe with the columns:
    1. product_category: The name of the products category
    2. total_amount: Total summed up amount lost per each product category
    3. revenue_leak_percentage: Their contribution to the total revenue leakage in %
    """

    return execute_query(conn=conn,
                         sql_path=sql_base_path / "order_cncl_per_category_amount.sql",
                         query_name="cncl_per_prod_category_amount",
                         expected_columns=['product_category', 'total_amount', 'revenue_leak_percentage'])



# -----------------------------------------------------------------------------------
# 6. Break down on canceled product category by total volume for VOLUME VS REVENUE Comparison:
# -----------------------------------------------------------------------------------

def get_cncl_by_prod_cat_volume(conn, sql_base_path:Path) -> pd.DataFrame:
    """
    This function will be responsible to return cancelation volume per the product categories:

    Returns:
    --------
    pd.Dataframe with the columns:
    1. product_category: The name of the products category
    2. total_n_orders: Total cancled orders 
    """

    return execute_query(conn=conn,
                         sql_path=sql_base_path / "order_cncl_per_category_volume.sql",
                         query_name="cncl_per_prod_category_volume",
                         expected_columns=['product_category', 'total_n_orders'])