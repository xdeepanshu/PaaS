FROM python:latest
RUN apt-get update
COPY ./requirements.txt /webapp/requirements.txt
WORKDIR /webapp
RUN pip install -r requirements.txt
ENV DOCKER_HOST=docker:2375