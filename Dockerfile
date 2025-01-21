# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r dependencies.txt

# Expose port 8080
EXPOSE 8080

# Command to run the application
CMD ["python", "app.py"]
#CMD ["python", "app-optional.py"]
