from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        user='postgres',
        password=os.environ['POSTGRES_PASSWORD'],
        database='postgres'
    )

    print("Connection to PostgreSQL successful!")
    # conn.close()
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    results = cursor.fetchall()
    formatted_results = []
    for row in results:
        order = {
            "order_id": row[0],
            "customer": {
                "name": row[1],
                "email": row[2],
                "address": row[3]
            },
            "product_name": row[4],
            "quantity": row[5],
            "order_date": row[6],
            "priority": row[7]
        }
        formatted_results.append(order)

    return jsonify(formatted_results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
