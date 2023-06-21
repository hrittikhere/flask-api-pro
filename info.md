docker exec -it postgres /bin/sh

docker run --name postgres --rm -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=4y7sV96vA9wv46VR -e PGDATA=/var/lib/postgresql/data/pgdata -v /tmp:/var/lib/postgresql/data -p 5432:5432 -it postgres:14.1-alpine


INSERT INTO orders (order_id, customer_name, customer_email, customer_address, product_name, quantity, order_date, priority) VALUES (12345, 'John Doe', 'johndoe@example.com', '123 Main St, Chennai, Tamil Nadu, 600004', 'Widget', 2, '2023-06-09', 'medium');

CREATE TABLE orders (
    order_id INTEGER,
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    customer_address VARCHAR(255),
    product_name VARCHAR(255),
    quantity INTEGER,
    order_date DATE,
    priority VARCHAR(255)
);
kubectl exec -it postgres-7454f995b-4j6zs --  psql -h localhost -U admin --password -p 5432 postgresdb


 kubectl exec -it postgres-7454f995b-4j6zs --  psql -h localhost -U postgres --password -p 5432 postgres