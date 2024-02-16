# Use an official Python runtime as a parent image
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

WORKDIR /affinitypropagation
ADD . /affinitypropagation

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y python3-pip

# Make port 80 available to the world outside this container
#EXPOSE 80

# Run app.py when the container launches
#CMD ["python", "app.py"]
