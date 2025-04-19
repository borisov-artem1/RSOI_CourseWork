FROM python:3.10-slim-buster

WORKDIR /statistics

COPY ./backend/src/statistics_service /statistics
COPY ./backend/config.yaml /statistics
COPY ./backend/src/requirements.txt /statistics

RUN pip3.10 install -r requirements.txt

EXPOSE 8090

CMD ["python3", "app/main.py"]
