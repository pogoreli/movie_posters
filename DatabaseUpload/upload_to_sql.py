import csv
import mysql.connector
import os
import re
from mysql.connector import errorcode
from mysql.connector import Error

# Define CSV file path
csv_file_path = 'G:\My Drive\Projects\movie_posters\Vectorization\Vectors\Vectors.csv'

# MySQL connection configuration
try:
    cnx = mysql.connector.connect(
        user=os.environ.get('SQL_USERNAME'),
        password=os.environ.get('SQL_PASSWORD'),
        host='localhost',
        database='movies_project'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The credentials you provided are incorrect.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")
    else:
        print(err)
    cnx = None

# Create SQL table creation queries
create_vectors_table_query = """
CREATE TABLE IF NOT EXISTS vectors (
    movie_id INT PRIMARY KEY REFERENCES movies(movie_id),
    """ + ", ".join([f"vec_{i} FLOAT NOT NULL" for i in range(256)]) + """
);
"""

# Function to create tables in MySQL
def create_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(create_vectors_table_query)
        connection.commit()
        print("Table created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

# Function to load data from CSV to MySQL
def load_data_from_csv_to_mysql(connection, csv_file_path):
    try:
        cursor = connection.cursor()
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                # Extract numerical value from "tensor(<value>)"
                movie_id_match = re.search(r'\d+', row[0])
                if movie_id_match:
                    movie_id = int(movie_id_match.group())
                else:
                    print(f"Error: Could not extract movie_id from row: {row[0]}")
                    continue

                # Extract vector values
                vector_values = list(map(float, row[1:]))

                # Debug: Verify the extracted values
                print(f"Debug: movie_id = {movie_id}, len(vector_values) = {len(vector_values)}")

                # Ensure that the number of vector values matches the number of columns in the table
                if len(vector_values) != 256:
                    raise ValueError(f"Incorrect number of vector values for movie_id {movie_id}. Expected 256, got {len(vector_values)}.")

                # Insert movie data with vector values
                insert_query = """
                INSERT INTO vectors (
                    movie_id, """ + ", ".join([f"vec_{i}" for i in range(256)]) + """
                ) VALUES (
                    %s, """ + ", ".join(["%s"] * 256) + """
                )
                """
                # Debug: Print the insert statement to verify its correctness
                print(f"Debug: insert_query = {insert_query}")

                cursor.execute(insert_query, (movie_id, *vector_values))

            connection.commit()
            print("Data loaded successfully.")
    except Error as e:
        print(f"Error loading data: {e}")
    except ValueError as ve:
        print(f"Data validation error: {ve}")
    finally:
        cursor.close()

# Main function
def main():
    if cnx is None:
        print("Database connection could not be established.")
        return
    
    try:
        # Establish MySQL connection
        connection = cnx
        if connection.is_connected():
            print("Connected to MySQL database.")

            # Create tables
            create_tables(connection)

            # Load data from CSV to MySQL
            load_data_from_csv_to_mysql(connection, csv_file_path)

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    main()
