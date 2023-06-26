import csv
import psycopg2
import os

# CSV file path
csv_file = 'MOCK_DATA.csv'

# Read the CSV file
def read_csv(csv_file):
    """Read the CSV file"""
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        data = list(reader)
        return data

# Connect to the database
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['POSTGRES_HOST'],
        user='postgres',
        password=os.environ['POSTGRES_PASSWORD'],
        database='postgres'
    )
    print("Connection to PostgreSQL successful!")
    return conn

conn = get_db_connection()
cur = conn.cursor()

# Create table
def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS orders (order_id integer, customer_name text, customer_email text, customer_address text, product_name text, quantity integer, order_date date, priority text)")
    print("Table created successfully")
    conn.commit()

# Write data to the database
def write_to_db():
    data = read_csv(csv_file)
    for user in data:
        print(user)
        id = user[0]
        first_name = user[1]
        email = user[2]
        address = user[3]
        product = user[4]
        quantity = user[5]
        date = user[6]
        priority = user[7]
        cur.execute("INSERT INTO orders (order_id, customer_name, customer_email, customer_address, product_name, quantity, order_date, priority) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (id, first_name, email, address, product, quantity, date, priority))

# Create the table and write data to the database
create_table()
write_to_db()

# Commit changes and close the connection
conn.commit()
conn.close()
