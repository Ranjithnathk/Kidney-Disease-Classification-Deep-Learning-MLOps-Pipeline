# Base image
FROM python:3.8-slim-buster

# Install required packages
RUN apt-get update && apt-get install -y \
    awscli \
    curl \
    && apt-get clean

# Set workdir
WORKDIR /app

# Copy all files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit and Flask ports
EXPOSE 8501
EXPOSE 5000

# Default command: Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# To run Flask:
# docker run -p 5000:5000 kidney-disease-classifier python flask_app.py
