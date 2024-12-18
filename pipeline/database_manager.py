from typing import List
import os
import argparse
import logging

from duckdb import DuckDBPyConnection
import duckdb as ddb

# Establishes a connection to the DuckDB database and sets up S3 credentials
def connect_to_database(path: str) -> DuckDBPyConnection:
    logging.info(f"Connecting to database at {path}")

    con = ddb.connect(path)
    # Setting S3 credentials (empty here as placeholders)
    con.sql("""
            SET s3_access_key_id='';
            SET s3_secret_access_key='';
            SET s3_region='';
        """)
    return con # Returning the database connection object

# Closes the DuckDB database connection
def close_database_connection(con: DuckDBPyConnection) -> None:
    logging.info(f"Closing database connection")

    con.close() # Closing the database connection

# Collects the paths of all SQL files in the specified parent directory and its subdirectories
def collect_query_paths(parent_dir: str) -> List[str]:
    sql_files = []

    # Walking through the directory tree to find .sql files
    for root, _, files in os.walk(parent_dir):
        for file in files:
            # Checking for SQL file extension
            if file.endswith(".sql"):
                file_path = os.path.join(root, file)
                sql_files.append(file_path)

    logging.info(f"Found {len(sql_files)} sql scripts at location {parent_dir}")
    
    return sorted(sql_files) # Returning the sorted list of SQL file paths

# Reads the content of an SQL file
def read_query(path: str) -> str:
    with open(path, "r") as f:
        query = f.read()
        f.close()
    return query # Returning the SQL query as a string

# Executes a single SQL query on the provided DuckDB connection
def execute_query(con: DuckDBPyConnection, query: str) -> None:
    con.execute(query) # Executing the SQL query on the database

# Sets up the database by running all SQL scripts in a specified directory
def setup_database(database_path: str, ddl_query_parent_dir: str) -> None:
    query_paths = collect_query_paths(ddl_query_parent_dir)

    con = connect_to_database(database_path)

    # Executing each query in the collected SQL files
    for query_path in query_paths:
        query = read_query(query_path)
        execute_query(con, query)
        logging.info(f"Executed query from {query_path}")
    
    close_database_connection(con)

# Deletes the database file if it exists
def destroy_database(database_path: str) -> None:
    if os.path.exists(database_path):
        os.remove(database_path) # Deleting the database file

# Main function for command-line interface
def main():
    logging.getLogger().setLevel(logging.INFO)

    # Defining command-line arguments
    parser = argparse.ArgumentParser(description="CLI tool to setup or destroy a database.")

    # Creating mutually exclusive options for creating or destroying the database
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--create", action="store_true", help="Create the database")
    group.add_argument("--destroy", action="store_true", help="Destroy the database")

    # Adding arguments for database path and query directory path
    parser.add_argument("--database-path", type=str, help="Path to the database")
    parser.add_argument("--ddl-query-parent-dir", type=str, help="Path to the parent directory of the ddl queries")

    args = parser.parse_args()

    # Handling the create and destroy options
    if args.create:
        setup_database(database_path=args.database_path, ddl_query_parent_dir=args.ddl_query_parent_dir)
    elif args.destroy:
        destroy_database(database_path=args.database_path)

if __name__ == "__main__":
    main()
