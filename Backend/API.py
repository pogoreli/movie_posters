import torch
import numpy as np
import os
from PIL import Image
from ImageVectorizer import ImageVectorizer  # Assuming ImageVectorizer is defined in image_vectorizer.py
from MovieVectorDatabase import MovieVectorDatabase  # Assuming MovieVectorDatabase is defined in movie_vector_database.py
from ImageVectorizer import CustomResNet  # Assuming CustomResNet is defined in custom_resnet.py

def get_movie_genres_from_image(image_input):
    # Step 1: Vectorize the image
    vectorizer = ImageVectorizer(device='cpu')  # Use CPU for simplicity
    image_vector = vectorizer.vectorize_image(image_input)
    
    # Step 2: Get the closest vector ID from the database
    db = MovieVectorDatabase()
    if not db.connection:
        print("Failed to connect to the database. Please check your credentials and database configuration.")
        return []
    
    closest_movie_id = db.get_closest_vector_id(image_vector)
    if closest_movie_id is None:
        print("No movie found in the database matching the provided image.")
        return []
    
    # Step 3: Get the genre indexes for the movie (handle case sensitivity)
    genre_indexes = db.get_movie_genres_indexes(closest_movie_id)
    if not genre_indexes:
        print("No genres found for the closest movie.")
        return []
    
    # Step 4: Get genre names by genre indexes (handle case sensitivity)
    genre_names = db.get_genre_names_by_indexes([index.lower() for index in genre_indexes])
    if not genre_names:
        print("Failed to retrieve genre names.")
    
    return genre_names


# Usage Example
if __name__ == "__main__":
    image_path = r"C:\Users\HomePC\Desktop\poster_image.jpg"  # Replace with your image path
    genres = get_movie_genres_from_image(image_path)
    print(f"Predicted Genres: {genres}")
