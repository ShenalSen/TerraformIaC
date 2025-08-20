# Dockerfile for Flask App
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV DB_HOST=mysql-db
ENV DB_USER=root
ENV DB_PASSWORD=password
ENV DB_DATABASE=webapp

CMD ["python", "app.py"]
