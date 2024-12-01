# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Copy the requirements file into the image
COPY requirements.txt /code/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the image at /code
COPY . /code/

# Run the Django development server
ENTRYPOINT [ "./entrypoint.sh" ]
