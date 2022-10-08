# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster as production

# Install dependencies in a virtualenv
ENV VIRTUAL_ENV=/venv

RUN useradd wagtail_space_liveblog --create-home && mkdir /app $VIRTUAL_ENV && chown -R wagtail_space_liveblog /app $VIRTUAL_ENV

WORKDIR /app

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE" command.
ENV PYTHONUNBUFFERED=1 \
    PATH=$VIRTUAL_ENV/bin:$PATH \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=wagtail_space_liveblog.settings.production \
    PORT=8000 \
    WEB_CONCURRENCY=3 \
    GUNICORN_CMD_ARGS="-k uvicorn.workers.UvicornWorker --max-requests 1200 --max-requests-jitter 50 --access-logfile - --timeout 25"

# Port used by this container to serve HTTP.
EXPOSE 8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

USER wagtail_space_liveblog

RUN python -m venv $VIRTUAL_ENV
RUN pip install --upgrade pip

# Install the application server.
RUN pip install "websockets"
RUN pip install "uvicorn"
RUN pip install "gunicorn==20.0.4"

# Install the project requirements.
COPY --chown=wagtail_space_liveblog requirements.txt /
RUN pip install -r /requirements.txt

# Copy the source code of the project into the container.
COPY --chown=wagtail_space_liveblog . .

# Collect static files.
RUN SECRET_KEY=none python manage.py collectstatic --noinput --clear

# Compress
RUN SECRET_KEY=none django-admin compress

# Start the application server.
CMD gunicorn wagtail_space_liveblog.asgi:application

FROM production as dev
