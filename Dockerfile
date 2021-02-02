FROM python:3.8-alpine

ARG POSTGRES_HOST
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

ENV POSTGRES_HOST=${POSTGRES_HOST}
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=${POSTGRES_DB}

# set working directory
WORKDIR /usr/src/app

# copy requirements.txt
COPY requirements.txt /usr/src/app/requirements.txt

# install dependencies
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 pip install --upgrade pip && pip install -r requirements.txt && \
 apk --purge del .build-deps

# add app
COPY . /usr/src/app

EXPOSE 80

CMD gunicorn -b 0.0.0.0:80 \
    --access-logfile /usr/src/app/_logs/access.log \
    --error-logfile /usr/src/app/_logs/error.log \
    --log-level debug \
    --reload \
    manage:app