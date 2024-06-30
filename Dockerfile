# Use the official Python image from the Docker Hub
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt requirements.txt

# Install the required dependencies
RUN pip install -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]