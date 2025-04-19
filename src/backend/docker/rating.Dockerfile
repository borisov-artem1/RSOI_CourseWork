FROM python:3.10-slim-buster

WORKDIR /rating

COPY ./backend/src/rating_service /rating
COPY ./backend/config.yaml /rating
COPY ./backend/src/requirements.txt /rating

RUN pip3.10 install -r requirements.txt

EXPOSE 8050

CMD ["python3", "app/main.py"]
