FROM python:3.9-alpine3.19
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
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
venv/bin/pip install -r /tmp/requirements.txt && \
rm -rf /tmp && \
    apk del .tmp-build-deps


RUN mkdir -p /vol/web/media && \
mkdir -p /vol/web/static && \
chmod -R 777 /vol && \
chmod -R +x /scripts

ENV DJANGO_SETTINGS_MODULE=app.settings
ENV PATH="/scripts:/py/bin:$PATH"


CMD ["run.sh"]
