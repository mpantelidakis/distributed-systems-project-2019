FROM python:3.7-alpine
MAINTAINER Minas Pantelidakis
# Goal : keep docker image to absolute minimum size

# It does not allow python to buffer outputs
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# use apk to add permanent dependencies
RUN apk add --update --no-cache postgresql-client jpeg-dev

# --virtual gives an alias to the dependencies so we can easily
# remove them after requirements have been installed
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt

# delete temporary dependencies
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# TODO share this volume with nginx
RUN mkdir -p /vol/web/media

# Javascript, css etc..
RUN mkdir -p /vol/web/static

# Create a user that will only run applications
RUN adduser -D user

# Change permission for media and static folders to user
RUN chown -R user:user /vol/

# The owner can do w/e with the directory
# And the rest can read & execute from the dir
RUN chmod -R 755 /vol/web

# Switch to that user
USER user

# If we don't execute the above lines of code, the image will run the app using root account.
# If someone compromises our app, gg qq .