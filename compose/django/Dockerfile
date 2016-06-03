FROM python:3.5

ENV PYTHONUNBUFFERED 1

# Copy this early so that the celery project can use the same layers
COPY . /app
# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

RUN pip install -U pip
RUN pip install -r /requirements/production.txt

RUN groupadd -r django && useradd -r -g django django
RUN chown -R django /app

COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN sed -i 's/\r//' /gunicorn.sh
RUN chmod +x /entrypoint.sh && chown django /entrypoint.sh
RUN chmod +x /gunicorn.sh && chown django /gunicorn.sh

RUN mkdir -p /data/staticfiles \
    && chown -R django /data/staticfiles \
    && chgrp -R django /data/staticfiles

VOLUME /data/staticfiles

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
