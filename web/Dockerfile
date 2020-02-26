FROM python:3.6.10-alpine

WORKDIR /root

COPY requirements.txt requirements.txt

RUN apk add postgresql-libs &&\
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir &&\
    apk --purge del .build-deps

COPY . .

RUN chmod +x ./start_server_script

EXPOSE $APP_PORT

CMD ./start_server_script
