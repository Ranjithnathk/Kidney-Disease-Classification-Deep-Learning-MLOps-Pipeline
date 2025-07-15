FROM python:3.8-slim-bullseye

WORKDIR /app
COPY . /app

# Install dependencies
RUN apt update -y && apt install -y curl awscli && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
EXPOSE 8501

# Use supervisord to run both Flask and Streamlit properly
RUN apt install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]
