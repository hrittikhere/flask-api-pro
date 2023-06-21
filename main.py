from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2


conn = psycopg2.connect(
    host='localhost',
    port=5432,
    user='postgres',
    password='4y7sV96vA9wv46VR',
    database='postgres'
)
print("Connection to PostgreSQL successful!")
# conn.close()
cursor = conn.cursor()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:4y7sV96vA9wv46VR@localhost:5432/postgres'
db = SQLAlchemy(app)


@app.route('/')
def index():
    cursor.execute("SELECT * FROM orders")
    results = cursor.fetchall()
    formatted_results = []
    for row in results:
        order = {
            "order_id": row[0],
            "customer": {
                "name": row[1],
                "email": row[2],
                "address": {
                    "street": row[3],
                    "city": row[4],
                    "state": row[5],
                    "postal_code": row[6]
                }
            },
            "product_name": row[7],
            "quantity": row[8],
            "order_date": row[9],
            "priority": row[10]
        }
        formatted_results.append(order)

    return jsonify(formatted_results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
