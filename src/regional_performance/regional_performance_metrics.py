import pandas as pd
from pathlib import Path
from utils.helper import execute_query


# --------------------------------
# Regional Performance Analysis Specific Wrappers:
# --------------------------------


# -----------------------------------------------------------------------------------
# 1. Get the total revenues by state:
# -----------------------------------------------------------------------------------

def get_rev_by_state_at_customer_level(conn, sql_base_path:Path) -> pd.DataFrame:
    """
    This function will be reponsible to generate spendings by each customer
    along with their address informations like zip-code, city, and state.

    Returns:
    --------
    pd.Dataframe with the revenue per customer along with their address information
    """

    return execute_query(conn=conn,
                         sql_path=sql_base_path / "baseline_performance.sql",
                         query_name="highest_revenue_by_state_w_customer_info",
                         expected_columns=['customer_unique_id', 'total_spending',
                                           'zip_code', 'city', 'state'])


# -----------------------------------------------------------------------------------
# 2. Get the total volume of orders by state:
# -----------------------------------------------------------------------------------

def get_order_vol_by_state_at_customer_level(conn, sql_base_path:Path) -> pd.DataFrame:
    """
    This function will be responsible to count the total number of orders per state at customer level

    Returns:
    -----------
    pd.Dataframe with the total number of distinct order counts by state at customer level
    """

    return execute_query(conn=conn,
                         sql_path=sql_base_path / "baseline_performance.sql",
                         query_name= "highest_volume_of_orders_by_state",
                         expected_columns=None)