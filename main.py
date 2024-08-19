from scripts import process_excel, clean_and_transform_data, db_operations
import json


def load_config(config_file='config.json'):
    # Load the configuration file
    with open(config_file, 'r') as f:
        config_main = json.load(f)
    return config_main


if __name__ == "__main__":
    # Load the configuration
    config = load_config()

    # 1. Process the Excel file
    process_excel.process_excel(config)

    # 2. Clean and transform the data
    cleaned_file = config['cleaned_students.csv']
    clean_and_transform_data.clean_and_transform_data(config['students.csv'], cleaned_file)

    # 3. Work with the database
    db_operations.main()

    print("Data processing completed successfully!")
