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

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['POSTGRES_HOST'],
        user='postgres',
        password=os.environ['POSTGRES_PASSWORD'],
        database='postgres'
    )

    print("Connection to PostgreSQL successful!")
    # conn.close()
    return conn

conn = get_db_connection()
cur = conn.cursor()

data = read_csv(csv_file)

def write_to_db(data):
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


write_to_db(data)
conn.commit()
conn.close()
