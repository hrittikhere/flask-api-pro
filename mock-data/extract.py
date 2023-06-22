import csv
import psycopg2
import os

# CSV file path
csv_file = 'MOCK_DATA.csv'

# read csv file


def read_csv(csv_file):
    """Read the CSV file"""
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        data = list(reader)
        return data

# connect to database


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

# create table


def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS orders (order_id integer, customer_name text, customer_email text, customer_address text, product_name text, quantity integer, order_date date, priority text)")
    print("Table created successfully")
    conn.commit()


# write to database
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
        priorty = user[7]
        cur.execute("INSERT INTO orders (order_id, customer_name, customer_email, customer_address , product_name, quantity, order_date, priority) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (id, first_name, email, address, product, quantity, date, priorty))


create_table()
write_to_db()

conn.commit()
conn.close()
