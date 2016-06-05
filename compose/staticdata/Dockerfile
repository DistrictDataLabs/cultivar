FROM python:3.5

VOLUME /staticfiles

RUN groupadd -r django \
  && useradd -r -g django django \
  && chown -R django /staticfiles

