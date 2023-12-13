FROM python:3.9-alpine3.13
LABEL maintainer="marcusdev"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ./app /app
COPY ./requirements.txt /tmp/requirements.txt
COPY ./scripts /scripts
EXPOSE 8000

RUN python -m venv venv && \
venv/bin/pip install --upgrade pip && \
apk  add --update --no-cache postgresql-client && \
apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev linux-headers && \
venv/bin/pip install -r /tmp/requirements.txt && \
rm -rf /tmp && \
    apk del .tmp-build-deps

ENV DJANGO_SETTINGS_MODULE=app.settings
ENV PATH="/scripts:/py/bin:$PATH"

USER brainbox

CMD ["run.sh"]
