FROM python:3.6.10-alpine

WORKDIR /root

COPY requirements.txt requirements.txt

ENV RVS_DB_NAME 'rvs_incrementer_db'
ENV RVS_DB_PORT '5432'
ENV RVS_DB_HOST 172.18.0.2
ENV RVS_DB_USER 'rvs_user'
ENV RVS_DB_PASS 'rvs_user'
ENV RVS_APP_PORT 8000
ENV RVS_APP_IP 0.0.0.0

RUN apk add postgresql-libs &&\
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir &&\
    apk --purge del .build-deps &&\
    apk add bash &&\
    apk add curl

COPY . .

RUN chmod +x ./start_server_script

EXPOSE $RVS_APP_PORT

CMD ./start_server_script
