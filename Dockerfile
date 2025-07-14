FROM python:3.8-slim-bullseye

WORKDIR /app

COPY . /app

RUN apt update -y && apt install -y curl awscli \
 && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "python flask_app.py & streamlit run app.py --server.port=8080 --server.enableCORS=false"]
