FROM python:3.10-slim-buster

WORKDIR /library

COPY ./backend/src/library_service /library
COPY ./backend/config.yaml /library
COPY ./backend/src/requirements.txt /library

# Попробуем по одному (или 2-3 за раз) — для теста
RUN pip install --no-cache-dir -r requirements.txt --timeout 600 -v

EXPOSE 8060

CMD ["python3", "app/main.py"]
