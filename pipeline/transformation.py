import argparse
import logging

# Importing utility functions for database management and query execution
from database_manager import (
    connect_to_database,
    close_database_connection,
    execute_query,
    collect_query_paths,
    read_query,
)

# Function to handle data transformation using a series of SQL queries
def transform_data(args) -> None:
    database_path = args.database_path
    con = connect_to_database(path=database_path)
    query_paths = collect_query_paths(args.query_directory)

    # Executing each query in the collected SQL files
    for query_path in query_paths:
        query = read_query(query_path)
        execute_query(con, query)

        logging.info(f"Executed query from {query_path}")

    close_database_connection(con)

# Main function to set up the CLI for the transformation script
def main():
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description="CLI for Data Transformation")
    parser.add_argument(
        "--database_path", type=str, required=True, help="Path to the DuckDB database"
    )
    parser.add_argument(
        "--query_directory",
        type=str,
        required=True,
        help="Directory containing SQL transformation queries",
    )

    args = parser.parse_args()
    transform_data(args)

if __name__ == "__main__":
    main()