# Flask API for Managing Orders Data

This Flask API allows users to manage orders data stored in a PostgreSQL database. The API provides endpoints for creating, reading, updating, and deleting orders.

## Prerequisites

Before setting up and running the Flask API application, ensure you have the following prerequisites installed:

- Docker
- Kubernetes (kubectl)
- PostgreSQL

## Setup

Follow the steps below to set up and run the Flask API application:

1. Clone the repository:

   ```shell
   $ git clone https://github.com/yourusername/flask-app.git
   $ cd flask-app
   ```

2. Build the Docker image for the Flask application:
   ```shell
   $ docker build -t flask-api .
   ```

3. Build the Docker image for the Mocker:
  ```shell
   $ docker build -t mock-data .
   ```

4. Create a Kubernetes cluster either in the cloud or locally. Make sure kubectl is configured to access the cluster.

5. Create a PostgreSQL database instance or use an existing one.

Install Helm:
   ```shell
   $ curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

Install Postgres: 
   ```shell
   $ helm repo add bitnami https://charts.bitnami.com/bitnami 
   $ helm install postgres bitnami/postgresql
   ```


6. Apply the Kubernetes manifests to deploy the Flask application and run job to store order data into the database:
   ```shell
   $ kubectl apply -f app.yml
   $ kubectl apply -f job.yml
   ```

7. Verify that the pods and services are running:
   ```shell
   $ kubectl get pods
   $ kubectl get svc   
   ```
   
8. Access the Flask API:

- Get the external IP address of the Flask application service:
   ```shell
   $ kubectl get svc flask-service
   ```

- Use tools like cURL or Postman to send HTTP requests to the API endpoints, using the obtained IP address. For example:
   ```shell
   $ curl http://<flask-service-external-ip>/orders
   ```

9. Test the API by making requests to different endpoints:

* Create a new order: POST /orders with the below json:
```json
  {
 "customer": {
   "name": "John Doe",
   "email": "johndoe@example.com",
   "address": "123 Main St, City, Country"
 },
 "order_id": 3433,
 "product_name": "Widget",
 "quantity": 5,
 "order_date": "2023-06-22",
 "priority": "high"
}
```
* Get an order: GET /order/<order_id>
* List all orders: GET /order
* Delete an order: DELETE /order/<order_id>
* Search an order with: Get /order/search

## Dependencies

The Flask API application has the following dependencies:

* Flask
* psycopg2

These dependencies are included in the requirements.txt file.

To install the dependencies locally, run the following command:
```bash
pip install -r app/requirements.txt mock-data/requirements.txt
```

## Additional Information

The Flask API handles errors and returns appropriate HTTP status codes:

* 404 - Not found if the data is not found
* 401 - Invalid request
* 405 - Method not allowed


