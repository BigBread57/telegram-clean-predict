# This Dockerfile uses multi-stage build to customize DEV and PROD images:
# https://github.com/wemake-services/wemake-django-template/

FROM python:3.11-slim-buster AS python

LABEL maintainer="mazur.gleb2010@yandex.ru"
LABEL vendor="gleb"

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# copy project
COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]