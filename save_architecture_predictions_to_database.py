import pandas as pd
import sqlite3

# Database
CSV_FILE = "software_arch_classification_20240128.csv"
DATABASE_TO_SAVE = 'merged_github_data_20240121_093434.db'

# Create table on the database
def create_architecture_predictions_table(conn):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS architecture_predictions (
        repository_id TEXT PRIMARY KEY,
        architecture_prediction_1 TEXT,
        architecture_prediction_2 TEXT,
        architecture_prediction_3 TEXT,
        best_of_3_predictions TEXT,
        FOREIGN KEY(repository_id) REFERENCES repositories(ID)
    )
    '''
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()

def main():
    print("Starting...")

    print("Connecting to the database...")
    conn = sqlite3.connect(DATABASE_TO_SAVE)

    print("Creating database tables...")
    create_architecture_predictions_table(conn)

    print("Reading the CSV file...")
    df = pd.read_csv(CSV_FILE)

    print("Extracting information from the CSV file...")
    # Mapping CSV columns to database table columns
    columns_mapping = {
        'repository id': 'repository_id',
        'architecture clasification 1': 'architecture_clasification_1',
        'architecture clasification 2': 'architecture_clasification_2',
        'architecture clasification 3': 'architecture_clasification_3',
        'Majority Vote': 'majority_vote'
    }
    # Selecting and renaming only the relevant columns
    df_selected = df[list(columns_mapping.keys())].rename(columns=columns_mapping)

    print("Saving to the database...")
    df_selected.to_sql('architecture_predictions', conn, if_exists='replace', index=False)

    print("Finished!")

if __name__ == "__main__":
    main()