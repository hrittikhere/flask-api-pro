from flask import Flask, jsonify, request
import psycopg2
import os
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        host=os.environ['POSTGRES_HOST'],
        user='postgres',
        password=os.environ['POSTGRES_PASSWORD'],
        database='postgres'
    )
    return conn


@app.route('/', methods=['GET'])
def all():
    """
    Retrieve all orders.
    ---
    responses:
      200:
        description: A list of orders.
    """
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


@app.route('/order/<int:order_id>', methods=['GET'])
def get_order_by_number(order_id):
    """
    Retrieve order details by order_id.
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: The ID of the order to retrieve.
    responses:
      200:
        description: The order with the specified ID.
      404:
        description: Order not found.
    """
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


@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    Delete an order by order_id.
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: The ID of the order to delete.
    responses:
      200:
        description: Order deleted successfully.
      404:
        description: Order not found.
    """
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


@app.route('/order', methods=['POST'])
def create_order():
    """
    Create a new order.
    ---
    parameters:
      - name: order_details
        in: body
        required: true
        schema:
          type: object
          properties:
            order_id:
              type: integer
              description: The ID of the order.
            customer:
              type: object
              properties:
                name:
                  type: string
                  description: The name of the customer.
                email:
                  type: string
                  description: The email of the customer.
                address:
                  type: string
                  description: The address of the customer.
              required:
                - name
                - email
                - address
            product_name:
              type: string
              description: The name of the product.
            quantity:
              type: integer
              description: The quantity of the product.
            order_date:
              type: string
              format: date
              description: The order date (YYYY-MM-DD).
            priority:
              type: string
              description: The priority of the order.
    responses:
      201:
        description: Order created successfully.
      401:
        description: Invalid request payload.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Extract order details from the JSON payload
        order_details = request.json
        order_id = order_details['order_id']
        customer = order_details['customer']
        product_name = order_details['product_name']
        quantity = order_details['quantity']
        order_date = order_details['order_date']
        priority = order_details['priority']

        # Insert the order into the database
        cursor.execute("INSERT INTO orders (order_id, customer_name, customer_email, customer_address, product_name, quantity, order_date, priority) VALUES (%s,%s, %s, %s, %s, %s, %s, %s) RETURNING order_id",
                       (order_id, customer['name'], customer['email'], customer['address'], product_name, quantity, order_date, priority))
        conn.commit()

        return jsonify({'order_id': order_id}), 201
    except KeyError:
        return jsonify({'error': 'Invalid request payload'}), 401
    except psycopg2.Error:
        return jsonify({'error': 'Failed to create order'}), 500


@app.route('/order/search', methods=['GET'])
def search_orders():
    """
    Search orders by product name.
    ---
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: The search query.
    responses:
      200:
        description: A list of orders matching the search query.
      500:
        description: Failed to retrieve orders.
    """
    try:
        # Get the search query from the query parameters
        search_query = request.args.get('q')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Retrieve the orders matching the search query from the database
        cursor.execute(
            "SELECT * FROM orders WHERE product_name LIKE %s", ('%' + search_query + '%',))
        orders = cursor.fetchall()

        if orders:
            # Create a list of dictionaries representing the matched orders
            orders_list = []
            for order in orders:
                order_dict = {
                    'order_id': order[0],
                    'customer_name': order[1],
                    'customer_email': order[2],
                    'customer_address': order[3],
                    'product_name': order[4],
                    'quantity': order[5],
                    'order_date': order[6],
                    'priority': order[7]
                }
                orders_list.append(order_dict)

            return jsonify({'orders': orders_list}), 200
        else:
            return jsonify({'message': 'No orders found matching the search query'}), 200

    except psycopg2.Error:
        return jsonify({'error': 'Failed to retrieve orders'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
