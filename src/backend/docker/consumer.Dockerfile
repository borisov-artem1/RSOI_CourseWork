FROM python:3.10-slim-buster

WORKDIR /consumer

COPY ./backend/src/consumer_service /consumer
COPY ./backend/config.yaml /consumer
COPY ./backend/src/requirements.txt /consumer

# Попробуем по одному (или 2-3 за раз) — для теста
RUN pip install --no-cache-dir -r requirements.txt --timeout 600 -v && echo "DONE installing" && sleep 5

CMD ["python3", "app/main.py"]
