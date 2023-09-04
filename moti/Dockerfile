# Use the official Python image from Docker Hub as a base image
FROM python:3.9

# Set environment variables for running Django in production
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=moti.settings

# Create and set the working directory inside the container
RUN mkdir /app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Expose the port the application runs on (default for Django is 8000)
EXPOSE 8000

CMD ["sh","-c","python moti/manage.py migrate && python moti/manage.py runserver 0.0.0.0:8000"]

