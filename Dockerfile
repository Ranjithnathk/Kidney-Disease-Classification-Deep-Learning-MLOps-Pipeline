FROM python:3.8-slim-bullseye

WORKDIR /app
COPY . /app

RUN apt update -y && apt install -y curl awscli supervisor
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000
EXPOSE 8501

CMD ["/usr/bin/supervisord"]
