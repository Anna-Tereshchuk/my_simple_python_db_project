import psycopg2
import json
# This script is created solely for educational purposes and to remove incorrect loads during the learning process.
# Use only when necessary.


def load_config(config_file='config.json'):
    # Load the configuration file
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config


def drop_students_table(conn):
    cur = conn.cursor()
    # Drop the table if it exists
    cur.execute("DROP TABLE IF EXISTS students")
    conn.commit()
    cur.close()
    print("Table 'students' successfully dropped.")


def main():

    # Load configuration
    config = load_config()

    # Connect to the database
    conn = psycopg2.connect(
        dbname=config['dbname'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )

    # Drop the table
    drop_students_table(conn)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
