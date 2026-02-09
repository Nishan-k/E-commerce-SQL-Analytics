import pandas as pd
from pathlib import Path
import sqlite3
from utils.helper import sql_loader, execute_query




# --------------------------------
# RFM Analysis Specific Wrappers:
# --------------------------------


# -----------------------------------------------------------------------------------
# 1. Create the temporary table `customer_order_info` to used for further analysis:
# -----------------------------------------------------------------------------------

def create_temp_table_customer_order_info(conn, sql_base_path):
    """
    This function will create a temporary table that will be useful for later stages.
    """

    try:        
        cursor = conn.cursor()    
    except Exception as e:
        raise (e)


    # Extract the queries based on the named queries:
    file_path = Path(sql_base_path) / "create_customer_order_table.sql"
    drop_query = sql_loader(file_path=file_path, query_name='drop_customer_order_table_if_exists')
    create_temp_table_query = sql_loader(file_path=file_path, query_name='create_temp_table')

    # Drop the tempoarry table if it exists:
    cursor.execute(drop_query)

    # # Create the temporary table:
    cursor.execute(create_temp_table_query)
    print(f"Temporary table `customer_order_info` successfully created !!")




# -----------------------------------------------------------------------------------
# 2. Recency Analysis
# -----------------------------------------------------------------------------------

def get_recency_analysis(conn, sql_base_path:Path) -> pd.DataFrame:
    """
    This function will be responsible to generate a recency table:

    Returns:
    --------
    pd.Dataframe with the recency information
    """

    return execute_query(conn=conn, 
                         sql_path=sql_base_path / "recency_analysis.sql",
                         query_name="recency_analysis",
                         expected_columns=['customer_id', 'latest_purchase_timestamp',
                                           'date_threshold', 'days_since_last_purchase', 'bins'])




# -----------------------------------------------------------------------------------
# 3. Frequency analysis
# -----------------------------------------------------------------------------------

def get_customer_order_frequency_analysis(conn, sql_base_path:Path) -> pd.DataFrame:
    """
    This function is responsible to return the order frequencies of the customers

    Returns:
    --------
    pd.Dataframe with the frequency count along with an interpretation
    """

    return execute_query(conn=conn,
                         sql_path=sql_base_path / "customer_order_frequency_interpretation.sql",
                         query_name="customer_order_frequency_interpretation",
                         expected_columns=["customer_unique_id", "total_orders", "Interpretation"])