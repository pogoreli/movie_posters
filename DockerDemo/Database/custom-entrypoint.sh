#!/bin/bash
set -e

# Start MySQL using the Bitnami entrypoint in the background
/opt/bitnami/scripts/mysql/entrypoint.sh /opt/bitnami/scripts/mysql/run.sh &

# Wait for MySQL to be fully up
echo "Waiting for MySQL to fully start..."
until mysqladmin ping -h "localhost" --silent; do
    sleep 5
done

# Add an extra delay to ensure MySQL has completed all setup tasks
sleep 10

# Run SQL files to populate the database
for file in /docker-entrypoint-initdb.d/*.sql; do
    if [[ "$file" != "/docker-entrypoint-initdb.d/custom-entrypoint.sh" ]]; then
        echo "Running $file"
        mysql -uroot -p"$MYSQL_ROOT_PASSWORD" < "$file" || {
            echo "Error running $file"
            exit 1
        }
    fi
done

# Bring MySQL to the foreground
wait
