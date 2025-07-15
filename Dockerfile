FROM python:3.8-slim-bullseye

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . /app

# Install essential system tools
RUN apt update -y && apt install -y curl awscli

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit (frontend) and Flask (backend) ports
EXPOSE 8080 5000

# Launch Flask and Streamlit apps in parallel
CMD ["sh", "-c", "python flask_app.py & streamlit run app.py --server.port=8080 --server.address=0.0.0.0 --server.enableCORS=false"]
