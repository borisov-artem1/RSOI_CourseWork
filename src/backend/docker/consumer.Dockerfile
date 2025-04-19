FROM python:3.10-slim-buster

WORKDIR /consumer

COPY ./backend/src/consumer_service /consumer
COPY ./backend/config.yaml /consumer
COPY ./backend/src/requirements.txt /consumer

RUN pip3.10 install -r requirements.txt

CMD ["python3", "app/main.py"]
