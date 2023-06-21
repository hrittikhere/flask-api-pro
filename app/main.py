from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os


app = Flask(__name__)

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI


db = SQLAlchemy(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:4y7sV96vA9wv46VR@localhost:5432/postgres'
# db = SQLAlchemy(app)


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
