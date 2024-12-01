# Use the official Python 3.9 image as a base
FROM python:3.10.15-slim


# Set the working directory in the container
WORKDIR /app

# Copy all the files from the backend folder to the container's working directory
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-cors numpy pillow mysql-connector-python pandas
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "API.py"]
