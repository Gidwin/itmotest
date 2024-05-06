FROM python:3.9-slim


WORKDIR /geo

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt  

