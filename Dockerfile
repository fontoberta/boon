FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev git libmysqlclient-dev
ENV PYTHONUNBUFFERED 1
ENV BOON_DB_USER root
ENV BOON_DB_PASSWORD rootpassword
ENV BOON_DB_NAME boon
ENV BOON_DB_PORT 3306
ENV BOON_DB_HOST db
RUN mkdir /code
ADD requirements.pip /code/
RUN pip3 install -r /code/requirements.pip
WORKDIR /code
ADD . /code/
ADD boon.service /etc/systemd/system/
