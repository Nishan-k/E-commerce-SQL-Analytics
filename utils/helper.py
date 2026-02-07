import re
from pathlib import Path
import sqlite3
import pandas as pd






# 1. A function to parse .sql files in case if it contains multiple queries:

def parse_sql_queries(file_path: str) -> dict:
    """
    This function is responsible for parsing SQL files with named query blocks.
    
    Parameters:
    -----------
    file_path: The path of the sql file

    Output:
    -----------
    returns a dictionary: {'query_name': 'QUERY'}
    """

    # Read the SQL file:
    with open(file_path, "r") as f:
        sql_content = f.read()

    
    # Split the queries by @query, here regular expression has been used:
    pattern = r'--\s*@query:\s*(\w+)\s*\n(.*?)(?=--\s*@query:|$)'
    matches = re.findall(pattern, sql_content, re.DOTALL)


    queries = {}
    for query_name, query_sql in matches:
        cleaned_sql = query_sql.strip()
        cleaned_sql = cleaned_sql.rstrip(';').strip()
        queries[query_name] = cleaned_sql
    
    return queries



# 2. A function that takes in the name defined for a specific query and returns it:

def get_query_from_file(file_path:str, query_name:str) -> str:
    """
    A function responsible to extract SQL query based on the name of the query provided.

    Parameters:
    -----------
    file_path: The path to the SQL file
    query_name: The name of the query that we want to extract
    """

    queries = parse_sql_queries(file_path)

    if query_name not in queries:
        raise ValueError(
            f"Query name: {query_name} not found, please pass the correct query name."
            f"Available query names: {list(queries.keys())}"
        )

    return queries[query_name]



# 3. To read a single query .sql file:

def read_single_sql_query(file_path:str):
    """
    This function reads the .sql files with only one query
    """

    with open(file_path, "r") as f:
        return f.read()
    


# # 4. To create a successful database connection:

# def create_db_connection():
#     db_path = "../data/ecommerce.db"
#     conn = sqlite3.connect(db_path)
#     return conn



# 5. Check duplicats:

def check_duplicates(sql_path:str, conn):
    """
    Checks for any duplicate rows
    """
    sql_path = Path(sql_path)
    query = get_query_from_file(sql_path, 'check_duplicates')
    result = pd.read_sql_query(query, conn)
    return result


# 6. Get the available table names:

def extract_table_names(sql_path:str, conn) -> pd.DataFrame:
    """
    Returns the available table names from the database:

    Parmeters:
    ----------
    conn: sqlite3.Connection for database connection
    file_path: path containing SQL files
 
    """

    # Read the SQL file:
    sql_path = Path(sql_path)
    sql_query = read_single_sql_query(file_path=sql_path)
    tables = pd.read_sql_query(sql_query, conn)

    # Validate the results:
    if len(tables) == 0:
        raise ValueError("No tables found.")
    
    return tables