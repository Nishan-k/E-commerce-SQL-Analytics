import re
from pathlib import Path
import pandas as pd
from typing import Optional, Set





# 1. A function to parse .sql files and return the query based on the provided query name:

def sql_loader(file_path: str, query_name: str) -> str:
    """
    Load a named SQL query from a .sql file.
    """

    with open(file_path, "r") as f:
        sql_content = f.read()

    pattern = r'--\s*@query:\s*(\w+)\s*\n(.*?)(?=--\s*@query:|$)'
    matches = re.findall(pattern, sql_content, re.DOTALL)

    queries = {}
    for found_query_name, query_sql in matches: 
        cleaned_sql = query_sql.strip().rstrip(';').strip()
        queries[found_query_name] = cleaned_sql

    if query_name not in queries:
        raise ValueError(
            f"Query name '{query_name}' not found.\n"
            f"Available queries: {list(queries.keys())}"
        )

    return queries[query_name]





# 2. A function responsible to execute the SQL Queries:

def execute_query(conn, sql_path:Path, query_name:str, expected_columns:Optional[Set[str]] = None) -> pd.DataFrame:
    """
    This function is responsible to execute a named SQL query from a SQL file
    """

    query = sql_loader(sql_path, query_name)
    df = pd.read_sql_query(query, conn)

    if df.empty:
        raise ValueError(f"Query: `{query_name}` in {sql_path} returned empty rows.")

    if expected_columns is None:
        pass    
    elif expected_columns != df.columns.tolist():        
        raise ValueError(f"Expected columns: {expected_columns}, got {set(df.columns)}")

    return df
    




# 5. Check duplicats:

def check_duplicates(conn) -> pd.DataFrame: 
    """
    Checks for any duplicate rows
    """
    sql_path = Path("../sql/check_duplicates.sql")

    with open(sql_path, "r") as f:
        sql_query = f.read()

    duplicates = pd.read_sql_query(sql_query, conn)
    
    return duplicates



# 6. Get the available table names:

def extract_table_names(conn) -> pd.DataFrame:
    """
    Returns the available table names from the database:

    Parmeters:
    ----------
    conn: sqlite3.Connection for database connection
    file_path: path containing SQL files
 
    """

    # Read the SQL file:
    sql_path = Path("../sql/get_table_names.sql")

    with open(sql_path, "r") as f:
        sql_query = f.read()
    tables = pd.read_sql_query(sql_query, conn)

    # Validate the results:
    if len(tables) == 0:
        raise ValueError("No tables found.")
    
    return tables