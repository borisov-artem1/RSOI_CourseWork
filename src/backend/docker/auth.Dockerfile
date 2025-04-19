FROM python:3.10-slim-buster

WORKDIR /auth

COPY ./backend/src/auth_service /auth
COPY ./backend/config.yaml /auth
COPY ./backend/src/requirements.txt /auth

RUN pip3.10 install -r requirements.txt

EXPOSE 8888

CMD ["python3", "app/main.py"]
