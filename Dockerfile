FROM python:3.6.10-alpine

WORKDIR /root

ENV RVS_DB_NAME="rvs_incrementer_db"
ENV RVS_PORT="5432"
ENV RVS_HOST="127.0.0.1"
ENV RVS_USER="rvs_user"
ENV RVS_PASS="rvs_user"

COPY requirements.txt requirements.txt

RUN apk add postgresql-libs &&\
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir &&\
    apk --purge del .build-deps

COPY . .

EXPOSE 8000
EXPOSE 5432

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
