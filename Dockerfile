# Use an official Python runtime as a base image
FROM python:3.8-slim-buster

# Install system packages required by Chrome and necessary for wget and unzip
RUN apt-get update && \
    apt-get install -y wget unzip && \
    # Download and setup Chrome
    wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chrome-linux64.zip && \
    unzip chrome-linux64.zip -d /usr/local/bin && \
    mv /usr/local/bin/chrome-linux64/chrome /usr/local/bin/ && \
    rm -r /usr/local/bin/chrome-linux64 && \
    # Download and setup Chromedriver
    wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin && \
    rm chromedriver-linux64.zip && \
    rm -r chromedriver-linux64 && \
    chmod +x /usr/local/bin/chromedriver && \
    # Clean up
    apt-get remove -y wget unzip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the environment variable for the PATH
ENV PATH="/usr/local/bin:${PATH}"
ENV CHROME_EXECUTABLE_PATH="/usr/local/bin/chrome"
ENV CHROMEDRIVER_EXECUTABLE_PATH="/usr/local/bin/chromedriver"

# Copy the current directory contents into the container at /app
COPY src/ /app/
COPY db/ /app/db/
COPY requirements.txt /app/

# Set the working directory in the container to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point to run main.py with parameters passed to docker run
ENTRYPOINT ["python", "main.py"]

# Define a volume for the database
VOLUME /app/db
