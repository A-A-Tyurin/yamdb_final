FROM python:3.8.5-alpine
WORKDIR /yamdb
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/yamdb/entrypoint_web.sh"]
CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000