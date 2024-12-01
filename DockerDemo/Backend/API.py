from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import numpy as np
import os
from PIL import Image
from ImageVectorizer import ImageVectorizer  # Assuming ImageVectorizer is defined in image_vectorizer.py
from MovieVectorDatabase import MovieVectorDatabase  # Assuming MovieVectorDatabase is defined in movie_vector_database.py
from ImageVectorizer import CustomResNet  # Assuming CustomResNet is defined in custom_resnet.py
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def get_movie_genres_from_image(image_input):
    # Step 1: Vectorize the image
    logger.info("Starting image vectorization.")
    vectorizer = ImageVectorizer(device='cpu')  # Use CPU for simplicity
    image_vector = vectorizer.vectorize_image(image_input)
    logger.info("Image vectorization completed.")
    
    # Step 2: Get the closest vector ID from the database
    logger.info("Connecting to the movie vector database.")
    db = MovieVectorDatabase()
    if not db.connection:
        logger.error("Failed to connect to the database. Please check your credentials and database configuration.")
        return []
    
    closest_movie_id = db.get_closest_vector_id(image_vector)
    if closest_movie_id is None:
        logger.warning("No movie found in the database matching the provided image.")
        return []
    logger.info(f"Closest movie ID found: {closest_movie_id}")
    
    # Step 3: Get the genre indexes for the movie (handle case sensitivity)
    logger.info("Retrieving genre indexes for the closest movie.")
    genre_indexes = db.get_movie_genres_indexes(closest_movie_id)
    if not genre_indexes:
        logger.warning("No genres found for the closest movie.")
        return []
    logger.info(f"Genre indexes retrieved: {genre_indexes}")
    
    # Step 4: Get genre names by genre indexes
    logger.info("Retrieving genre names from genre indexes.")
    genre_names = db.get_genre_names_by_indexes(genre_indexes)
    if not genre_names:
        logger.warning("Failed to retrieve genre names.")
    else:
        logger.info(f"Genres retrieved: {genre_names}")
    
    return genre_names

@app.route('/')
def home():
    logger.info("Home endpoint accessed.")
    return "Welcome to the Movie Genre Prediction API! Use the /predict-genres endpoint to predict genres from an image.", 200

@app.route('/predict-genres', methods=['POST'])
def predict_genres():
    logger.info("/predict-genres endpoint accessed.")
    if 'image' not in request.files:
        logger.error("No image file provided in the request.")
        return jsonify({'error': 'No image file provided'}), 400
    
    image_file = request.files['image']
    try:
        logger.info("Opening the provided image file.")
        image = Image.open(image_file)
        genres = get_movie_genres_from_image(image)
        if not genres:
            logger.error("Could not determine genres for the provided image.")
            return jsonify({'error': 'Could not determine genres for the provided image'}), 500
        logger.info(f"Predicted genres: {genres}")
        return jsonify({'genres': genres}), 200
    except Exception as e:
        logger.exception("An error occurred while processing the image.")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)