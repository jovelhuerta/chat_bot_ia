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


# Set the environment variable for your virtual environment
#ENV VIRTUAL_ENV=/app/.venv

# Create the virtual environment
#RUN python3 -m venv $VIRTUAL_ENV

# Activate the virtual environment
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"
EXPOSE 5000
# Define the command to run your application
CMD ["python", "src/main.py"]