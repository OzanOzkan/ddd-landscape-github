import sqlite3
import glob
import utils.logger as logger
import utils.databasemanager as databasemanager
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def merge_databases():
    logger.print_with_timestamp("Merging data...")
    
    output_dir = '_output/'
    main_db_file = f'{output_dir}merged_github_data_{get_timestamp()}.db'

    # Get a list of all SQLite databases
    db_files = glob.glob(f'{output_dir}/github_data_*.db')

    # Open the main database
    main_conn = sqlite3.connect(main_db_file)

    # Create tables
    databasemanager.create_database_tables(main_conn)

    tables = ['repositories', 'topics', 'readme', 'commits', 'pull_requests', 'pull_request_comments', 'issues', 'issue_comments', "loc_data", "files"]

    for db_file in db_files:
        # Don't merge the main database with itself
        if db_file == main_db_file:
            continue

        logger.print_with_timestamp(f"Merging {db_file}")

        try:
            # Attach the secondary database to the main database
            main_conn.execute(f"ATTACH DATABASE '{db_file}' AS db_to_merge")

            # Merge each table
            for table in tables:
                main_conn.execute("BEGIN")
                
                columns = "*"
                statement = f"INSERT INTO main.{table} SELECT {columns} FROM db_to_merge.{table}"
                if table != "repositories":
                    # Get column names
                    cursor = main_conn.cursor()
                    cursor.execute(f"PRAGMA db_to_merge.table_info({table})")
                    columns = [row[1] for row in cursor.fetchall() if row[1] != 'ID']  # Exclude 'ID'
                    columns_string = ', '.join(columns)

                    # Perform the merge excluding the 'ID' column
                    statement = f"INSERT INTO main.{table}({columns_string}) SELECT {columns_string} FROM db_to_merge.{table}"

                main_conn.execute(statement)
                main_conn.execute("COMMIT")

        except sqlite3.IntegrityError as e:
            logger.print_with_timestamp(f"Unique constraint failed. Skipping this database and moving to the next one.: {e}")
            main_conn.execute("ROLLBACK")
            continue

        finally:
            # Detach the secondary database
            main_conn.execute("DETACH DATABASE 'db_to_merge'")

            # Remove the merged database file
            #os.remove(db_file)

    main_conn.close()

    logger.print_with_timestamp("Merging complete!")

def main():
    merge_databases()

if __name__ == "__main__":
    main()