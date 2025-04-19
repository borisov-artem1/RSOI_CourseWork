FROM python:3.10-slim-buster

WORKDIR /reservation

COPY ./backend/src/reservation_service /reservation
COPY ./backend/config.yaml /reservation
COPY ./backend/src/requirements.txt /reservation

RUN pip3.10 install -r requirements.txt

EXPOSE 8070

CMD ["python3", "app/main.py"]
