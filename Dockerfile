# Use a slim base image to reduce image size
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt setup.py ./

# Install dependencies explicitly to verify correct installation
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expone el puerto que Google Cloud Run usará
EXPOSE 8080

# Establece la variable de entorno para el puerto
ENV PORT 8080

# Define the command to run your application
CMD ["python", "src/main.py"]