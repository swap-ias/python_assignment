FROM tiangolo/uvicorn-gunicorn:python3.8-slim

ENV APP=/app \
    MODULE_NAME=app \
    PORT=5000

WORKDIR $APP

EXPOSE 5000

COPY ./requirements.txt $APP

RUN pip install --upgrade pip && \
  pip install -r requirements.txt

COPY ./financial/ $APP/
COPY *.py $APP/
