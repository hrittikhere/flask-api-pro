from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)


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

# Get all orders 
@app.route('/')
def all():
    try:
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
    except psycopg2.Error:
        return jsonify({'error': 'Failed to retrieve order'}), 500

# Get order details by order_id
@app.route('/orders/<order_id>', methods=['GET'])
def get_order_by_number(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Retrieve the order from the database
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()

        if order:
            # Format the order as a dictionary
            formatted_order = {
                "order_id": order[0],
                "customer": {
                    "name": order[1],
                    "email": order[2],
                    "address": order[3]
                },
                "product_name": order[4],
                "quantity": order[5],
                "order_date": order[6],
                "priority": order[7]
            }
            return jsonify(formatted_order), 200
        else:
            return jsonify({'error': 'Order not found'}), 404
    except psycopg2.Error:
        return jsonify({'error': 'Failed to retrieve order'}), 500

# Delete an order by order_id
@app.route('/order/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()

        if order:
            cursor.execute(
                "DELETE FROM orders WHERE order_id = %s", (order_id,))
            conn.commit()
            return jsonify({'message': 'Order deleted successfully'})
        else:
            return jsonify({'error': 'Order not found'}), 404
    except psycopg2.Error:
        return jsonify({'error': 'Failed to delete order'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
