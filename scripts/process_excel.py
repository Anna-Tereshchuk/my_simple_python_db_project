
import pandas as pd
import json
import phonenumbers
import os


def load_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        config_script = json.load(f)
    return config_script


def format_phone_number(phone_number, default_region='', format_type='INTERNATIONAL'):
    cleaned_number = ''  # Initialize cleaned_number to avoid referencing before assignment
    try:
        cleaned_number = ''.join(filter(str.isdigit, phone_number))

        if len(cleaned_number) < 10:
            cleaned_number = cleaned_number.zfill(10)

        if len(cleaned_number) > 10:
            cleaned_number = cleaned_number[:10]

        parsed_number = phonenumbers.parse(cleaned_number, default_region)

        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, getattr(phonenumbers.PhoneNumberFormat, format_type))
        else:
            return cleaned_number

    except phonenumbers.NumberParseException:
        return cleaned_number


def process_excel(config_script):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_file = os.path.join(script_dir, config_script['students.xlsx'])
    csv_file = os.path.join(script_dir, config_script['students.csv'])

    try:
        column_names = ['student_name', 'age', 'average_mark', 'gender', 'phone_number']

        # Read data with headers
        df = pd.read_excel(excel_file, header=0, names=column_names, dtype={'phone_number': str})

        df['phone_number'] = df['phone_number'].astype(str)

        df['phone_number'] = df['phone_number'].apply(lambda x: format_phone_number(x) if x.strip() else None)

        # Check if the file exists and remove its content
        if os.path.exists(csv_file):
            open(csv_file, 'w').close()

        # Save to CSV with headers, but don't write index
        df.to_csv(csv_file, index=False, encoding='utf-8-sig', header=True)
        print(f"CSV file created successfully: {csv_file}")
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
    except PermissionError as e:
        print(f"Error: Insufficient access rights: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    config = load_config()
    process_excel(config)
