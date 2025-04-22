FROM python:3.10-slim-buster

WORKDIR /statistics

COPY ./backend/src/statistics_service /statistics
COPY ./backend/config.yaml /statistics
COPY ./backend/src/requirements.txt /statistics

# Попробуем по одному (или 2-3 за раз) — для теста
RUN pip install --no-cache-dir -r requirements.txt --timeout 600 -v

EXPOSE 8090

CMD ["python3", "app/main.py"]
