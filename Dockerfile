FROM python:3.8-slim-bullseye

WORKDIR /app

COPY . /app

# Update apt and install tools
RUN apt update -y && apt install -y curl awscli

# Upgrade pip and setuptools to avoid conflicts
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Start both Flask (backend) and Streamlit (frontend)
CMD ["sh", "-c", "python flask_app.py & streamlit run app.py --server.port=8080 --server.enableCORS=false"]
