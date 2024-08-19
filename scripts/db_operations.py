import psycopg2
import pandas as pd
import json
import uuid


def load_config(config_file='config.json'):
    # Load the configuration file
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Check if 'dbname' key is in the configuration
    if 'dbname' not in config:
        raise ValueError("Missing 'dbname' key in config.json")

    return config


def create_students_table(conn):
    cur = conn.cursor()
    # Activate the uuid-ossp extension
    cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    # Create the students table if it does not exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,  -- Primary key and unique identifier
            first_name TEXT,
            second_name TEXT,
            average_mark NUMERIC(5,2),
            gender TEXT,
            phone_number TEXT
        )
    """)
    conn.commit()
    cur.close()


def clear_table(conn):
    cur = conn.cursor()
    # Clear all rows from the students table
    cur.execute("TRUNCATE TABLE students")
    conn.commit()
    cur.close()


def insert_data(conn, data):
    cur = conn.cursor()
    # Insert data into the students table
    for index, row in data.iterrows():
        student_id = str(uuid.uuid4())  # Generate a new UUID for each record
        cur.execute("""
            INSERT INTO students (student_id, first_name, second_name, average_mark, gender) 
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (student_id) DO NOTHING  -- Ignore conflicts with existing UUIDs
        """, (student_id, row['first_name'], row['second_name'], row['average_mark'], row['gender']))
    conn.commit()
    cur.close()


def count_students_by_gender_and_mark(conn):
    cur = conn.cursor()
    # Count the number of students by gender with an average mark greater than 5
    cur.execute("""
        SELECT gender, COUNT(*) AS count
        FROM students
        WHERE average_mark > 5
        GROUP BY gender;
    """)
    result = cur.fetchall()
    cur.close()
    return result


def main():
    # Load the configuration
    config = load_config()

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=config['dbname'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )

    # Create the students table
    create_students_table(conn)

    # Clear the table before inserting new data
    clear_table(conn)

    # Load cleaned data from the CSV file
    cleaned_students_key = 'cleaned_students.csv'
    if cleaned_students_key not in config:
        raise ValueError(f"Missing '{cleaned_students_key}' key in config.json")

    data = pd.read_csv(config[cleaned_students_key])

    # Insert data into the students table
    insert_data(conn, data)

    # Count students by gender and average mark, and display the result
    result = count_students_by_gender_and_mark(conn)
    df = pd.DataFrame(result, columns=['gender', 'count'])
    print(df)

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    main()
