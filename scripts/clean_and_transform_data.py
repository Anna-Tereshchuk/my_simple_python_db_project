
import pandas as pd
import json
import os


def load_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        config_script = json.load(f)
    return config_script


def clean_and_transform_data(input_csv, output_csv):
    # Check if the output file exists and remove its content
    if os.path.exists(output_csv):
        open(output_csv, 'w').close()

    # Load the CSV
    df = pd.read_csv(input_csv)

    # 1. Remove rows with missing 'average mark'
    df = df.dropna(subset=['average_mark'])

    # 2. Split 'student_name' into 'first_name' and 'second_name'
    df[['first_name', 'second_name']] = df['student_name'].str.split(' ', expand=True)
    df = df.drop(columns=['student_name'])  # Remove 'student_name' field

    # Create directory if it does not exist
    output_dir = os.path.dirname(output_csv)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save cleaned data
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Data cleaned and saved to {output_csv}")


if __name__ == "__main__":
    config = load_config()

    input_file = config['students.csv']  # Input CSV file
    output_file = config['cleaned_students.csv']  # File to save cleaned data

    if not os.path.exists(input_file):
        print(f"File {input_file} not found.")
        exit(1)

    clean_and_transform_data(input_file, output_file)
