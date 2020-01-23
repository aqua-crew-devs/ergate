FROM python:3.7-buster

USER root

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install dos2unix

EXPOSE 5000
ENV FLASK_APP=ergate

ENTRYPOINT [ "entrypoint.sh" ]