FROM python:3.7

WORKDIR /app

RUN apt-get update -u && apt-get install

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
