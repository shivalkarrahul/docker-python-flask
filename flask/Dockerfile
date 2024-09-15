# Use the official Python 3.7 image based on Alpine Linux, which is lightweight and minimal
FROM python:3.7-alpine

# Create a new directory called '/app' inside the container to hold the application code
RUN mkdir /app

# Set the working directory to '/app' so that all subsequent commands will be executed in this directory
WORKDIR /app

# Copy the 'requirements.txt' file from your local machine to the '/app' directory in the container
ADD requirements.txt /app

# Copy the 'main.py' file from your local machine to the '/app' directory in the container
ADD main.py /app

# Install the required Python libraries listed in 'requirements.txt' using pip
RUN pip3 install -r requirements.txt

# Define the command to run the application using Gunicorn:
# - "gunicorn": the WSGI HTTP server for Python web applications
# - "-w 4": use 4 worker processes to handle requests
# - "-b 0.0.0.0:8000": bind the application to all network interfaces on port 8000
# - "main:app": tells Gunicorn to run the 'app' object from the 'main' module (main.py)
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "main:app"]
