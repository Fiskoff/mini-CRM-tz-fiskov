FROM python:3.13.5

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt