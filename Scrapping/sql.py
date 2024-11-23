import mysql.connector
from mysql.connector import errorcode
import os
from movie import Movie

class SQL:
    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(
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

        self.cursor = self.cnx.cursor()

    def initialize(self):
        TABLES = {}

        TABLES['movies'] = (
            """
            CREATE TABLE IF NOT EXISTS movies (
                movie_id INT AUTO_INCREMENT PRIMARY KEY,
                movie_name VARCHAR(255) NOT NULL,
                movie_poster LONGBLOB
            )
            """
        )

        TABLES['genres'] = (
            """
            CREATE TABLE IF NOT EXISTS genres (
                genre_id INT AUTO_INCREMENT PRIMARY KEY,
                genre_name VARCHAR(250) NOT NULL
            )
            """
        )

        TABLES['movie_genres'] = (
            """
            CREATE TABLE IF NOT EXISTS movie_genres (
                movie_id INT NOT NULL,
                genre_id INT NOT NULL,
                PRIMARY KEY (movie_id, genre_id),
                FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
                    ON DELETE CASCADE
            )
            """
        )

        # Create each table
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print(f"Creating table '{table_name}'...", end='')
                self.cursor.execute(table_description)
                print("Done.")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Already exists.")
                else:
                    print(f"Failed: {err.msg}")
                    raise

        # Commit the changes
        self.cnx.commit()

    def insert_genre(self, genre_name):
        if not self.cursor or not self.cnx:
            print("No database connection.")
            return None
            
        try:
            # Check if the genre already exists
            select_query = "SELECT genre_id FROM genres WHERE genre_name = %s"
            self.cursor.execute(select_query, (genre_name,))
            result = self.cursor.fetchone()

            if result:
                # Genre exists, return its ID
                genre_id = result[0]
                print(f"Genre '{genre_name}' already exists with ID {genre_id}.")
            else:
                # Genre does not exist, insert it
                insert_query = "INSERT INTO genres (genre_name) VALUES (%s)"
                self.cursor.execute(insert_query, (genre_name,))
                self.cnx.commit()
                genre_id = self.cursor.lastrowid
                print(f"Inserted genre '{genre_name}' with ID {genre_id}.")

            return genre_id

        except mysql.connector.Error as err:
            print(f"Error inserting genre '{genre_name}': {err}")
            return None
        
    def connect_movie_to_genre(self, movie_id, genre_id):
        try:
            insert_query = "INSERT IGNORE INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)"
            self.cursor.execute(insert_query, (movie_id, genre_id))
            self.cnx.commit()
            if self.cursor.rowcount == 0:
                print(f"Connection between movie ID {movie_id} and genre ID {genre_id} already exists. Ignored insertion.")
            else:
                print(f"Connected movie ID {movie_id} with genre ID {genre_id}.")
        except mysql.connector.Error as err:
            print(f"Error connecting movie ID {movie_id} with genre ID {genre_id}: {err}")

    def insert_movie(self, movie):
        if not self.cursor or not self.cnx:
            print("No database connection.")
            return None
        
        name = movie.name
        genres = movie.genre
        poster = movie.poster

        try:
            select_query = "SELECT movie_id FROM movies WHERE movie_name = %s"
            self.cursor.execute(select_query, (name,))
            result = self.cursor.fetchone()

            if result:
                movie_id = result[0]
                print(f"Movie '{name}' already exists with ID {movie_id}.")
            else:
                insert_query = "INSERT INTO movies (movie_name, movie_poster) VALUES (%s, %s)"
                self.cursor.execute(insert_query, (name, poster,))
                self.cnx.commit()
                movie_id = self.cursor.lastrowid
                print(f"Inserted movie '{name}' with ID {movie_id}.")

        except mysql.connector.Error as err:
            print(f"Error inserting movie '{name}': {err}")
            return None

        genre_ids = []
        for genre in genres:
            genre_ids.append(self.insert_genre(genre))

        for genre_id in genre_ids:
            self.connect_movie_to_genre(movie_id, genre_id)

        return movie_id