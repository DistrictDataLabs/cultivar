FROM python:3.5

ENV PYTHONUNBUFFERED 1

# Copy this early so that the celery project can use the same layers
COPY . /app
# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

RUN pip install -U pip
RUN pip install -r /requirements/celery_prod.txt

RUN groupadd -r django && useradd -r -g django django
RUN chown -R django /app

WORKDIR /app

USER django