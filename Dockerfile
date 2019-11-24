FROM python:3-stretch
RUN rm -rf /usr/share/doc/*
ADD . /app
WORKDIR /app
RUN pip --no-cache-dir install -r requirements
