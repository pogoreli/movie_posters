import mysql.connector
import numpy as np
import os
from mysql.connector import errorcode

class MovieVectorDatabase:
    def __init__(self):
        # Establish the database connection
        try:
            self.connection = mysql.connector.connect(
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
            self.connection = None
        
    def __del__(self):
        # Close the database connection when the instance is deleted
        if self.connection:
            self.connection.close()

    def get_closest_vector_id(self, input_vector):
        # Ensure input_vector is a NumPy array
        if not isinstance(input_vector, np.ndarray):
            raise ValueError("input_vector must be a numpy array")
        
        if not self.connection:
            print("No database connection.")
            return None
        
        cursor = self.connection.cursor()
        
        # Construct the query to calculate Euclidean distance
        n = len(input_vector)
        query = """
            SELECT movie_id, SQRT(
        """
        
        # Add each dimension's distance contribution to the query
        distance_terms = [f"POW(vec_{i} - {input_vector[i]}, 2)" for i in range(n)]
        query += " + ".join(distance_terms)
        query += " ) AS distance FROM vectors ORDER BY distance ASC LIMIT 1;"
        
        # Execute the query
        cursor.execute(query)
        result = cursor.fetchone()
        
        # Close the cursor
        cursor.close()
        
        # Return the movie_id of the closest vector
        if result:
            return int(result[0])
        else:
            raise ValueError("No vectors found in the database")

    def get_movie_genres_indexes(self, movie_id):
        if not self.connection:
            print("No database connection.")
            return []
        
        cursor = self.connection.cursor()
        try:
            query = """
                SELECT genre_id
                FROM movie_genres
                WHERE movie_id = %s;
            """
            cursor.execute(query, (movie_id,))
            results = cursor.fetchall()
            genre_ids = [row[0] for row in results]
            return genre_ids
        except mysql.connector.Error as err:
            print(f"Error retrieving genres for movie ID {movie_id}: {err}")
            return []
        finally:
            cursor.close()

    def get_genre_names_by_indexes(self, genre_ids):
        if not self.connection:
            print("No database connection.")
            return []
        
        cursor = self.connection.cursor()
        try:
            format_strings = ','.join(['%s'] * len(genre_ids))
            query = f"""
                SELECT genre_name
                FROM genres
                WHERE genre_id IN ({format_strings})
                ORDER BY genre_id;
            """
            cursor.execute(query, tuple(genre_ids))
            results = cursor.fetchall()
            genre_names = [row[0] for row in results]
            return genre_names
        except mysql.connector.Error as err:
            print(f"Error retrieving genre names: {err}")
            return []
        finally:
            cursor.close()

# Example usage
if __name__ == "__main__":
    db = MovieVectorDatabase()
    input_vector = np.array([3.0, 5.2, 7.1] + [0.0] * 253)  # Adjusted for 256 dimensions
    closest_id = db.get_closest_vector_id(input_vector)
    if closest_id is not None:
        print("Closest vector ID:", closest_id)
        genres = db.get_movie_genres_indexes(closest_id)
        print("Genres for the closest movie (IDs):", genres)
        genre_names = db.get_genre_names_by_indexes(genres)
        print("Genres for the closest movie (Names):", genre_names)
