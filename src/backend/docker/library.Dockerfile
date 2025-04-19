FROM python:3.10-slim-buster

WORKDIR /library

COPY ./backend/src/library_service /library
COPY ./backend/config.yaml /library
COPY ./backend/src/requirements.txt /library

RUN pip3.10 install -r requirements.txt

EXPOSE 8060

CMD ["python3", "app/main.py"]
