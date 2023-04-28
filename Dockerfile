# Use the official Python image for ARM architecture
FROM arm32v7/python:3.9.16-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN apt-get update && \
    apt-get install -y libportaudio2 libsndfile1 && \
    pip install --index-url=https://www.piwheels.org/simple -r requirements.txt

# Copy the rest of the project files to the container
COPY . .

# Set the entry point command to run the Python script
CMD ["python", "app.py"]

