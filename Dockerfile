FROM python:3.8-slim-bullseye

WORKDIR /app
COPY . /app

# Install required tools and supervisor
RUN apt update -y && apt install -y curl awscli supervisor

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Create log directory for supervisord
RUN mkdir -p /var/log/supervisor

# Copy supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports for Flask and Streamlit
EXPOSE 5000
EXPOSE 8501

# Run both Flask and Streamlit via supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
