import mysql.connector
from mysql.connector import errorcode
import os
import numpy as np
import pandas as pd

# Establish database connection
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
    exit(1)  # Exit if connection fails

cursor = cnx.cursor()

# Function to get total number of genres
def get_total_genres():
    if not cursor or not cnx:
        print("No database connection.")
        return None

    try:
        query = "SELECT COUNT(*) AS total_genres FROM genres;"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            total_genres = result[0]
            print(f"Total number of genres: {total_genres}")
            return total_genres
        else:
            print("Failed to retrieve the total number of genres.")
            return None
    except mysql.connector.Error as err:
        print(f"Error retrieving total genres: {err}")
        return None

# Function to get all genres with their IDs and names
def get_all_genres():
    if not cursor or not cnx:
        print("No database connection.")
        return []
    try:
        query = "SELECT genre_id, genre_name FROM genres ORDER BY genre_id;"
        cursor.execute(query)
        results = cursor.fetchall()
        genres = [{'genre_id': row[0], 'genre_name': row[1]} for row in results]
        print(f"All genres retrieved.")
        return genres
    except mysql.connector.Error as err:
        print(f"Error retrieving all genres: {err}")
        return []

# Function to get genre IDs for a specific movie
def get_movie_genres_indexes(movie_id):
    if not cursor or not cnx:
        print("No database connection.")
        return []
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

# Function to get all movie data
def get_all_movie_data():
    if not cursor or not cnx:
        print("No database connection.")
        return []
    try:
        query = """
            SELECT movie_id, movie_name, movie_poster
            FROM movies
            ORDER BY movie_id;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        movies = [{'movie_id': row[0], 'movie_name': row[1], 'movie_poster': row[2]} for row in results]
        print(f"Total number of movies: {len(movies)}")
        return movies
    except mysql.connector.Error as err:
        print(f"Error retrieving all movie data: {err}")
        return []

# Encoding function
def encode(total, indexes):
    encoded = np.zeros(total, dtype=int)
    for idx in indexes:
        # Adjust idx to zero-based index if necessary
        if idx in genre_id_to_index:
            zero_based_idx = genre_id_to_index[idx]
            encoded[zero_based_idx] = 1
        else:
            print(f"Warning: Genre ID {idx} not found in genre_id_to_index mapping.")
    return encoded

# Main execution
if __name__ == "__main__":
    # Get total number of genres
    number_of_genres = get_total_genres()

    # Get all genres and create mappings
    genres = get_all_genres()
    # Mapping from genre_id to zero-based index
    genre_id_to_index = {genre['genre_id']: idx for idx, genre in enumerate(genres)}
    # List of genre names in order of indices
    genre_names = [genre['genre_name'] for genre in genres]

    # Get all movie data
    movies = get_all_movie_data()

    # Prepare data
    data = []

    for movie in movies:
        movie_id = movie['movie_id']
        movie_name = movie['movie_name']
        movie_poster = movie['movie_poster']  # Binary data

        # Get the genre IDs for the movie
        genre_ids = get_movie_genres_indexes(movie_id)
        # Encode the genre indexes
        encoded_genres = encode(number_of_genres, genre_ids)
        # Convert encoded_genres to list
        encoded_genres_list = encoded_genres.tolist()
        # Append to data
        data.append({
            'movie_id': movie_id,
            'movie_name': movie_name,
            'movie_poster': movie_poster,
            'genres_encoded': encoded_genres_list
        })

    # Create DataFrame
    df = pd.DataFrame(data)

    # Expand 'genres_encoded' into separate columns
    genres_df = pd.DataFrame(df['genres_encoded'].tolist(), columns=genre_names)

    # Concatenate 'movie_id', 'movie_name', 'movie_poster', and genre columns
    df_final = pd.concat([df[['movie_id', 'movie_name', 'movie_poster']], genres_df], axis=1)

    # Save the DataFrame to Parquet
    df_final.to_parquet('movies_genres_encoded.parquet', index=False)
    print("DataFrame saved to 'movies_genres_encoded.parquet'.")

    # Close the database connection
    cursor.close()
    cnx.close()
