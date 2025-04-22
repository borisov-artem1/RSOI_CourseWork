FROM python:3.10-slim-buster

WORKDIR /rating

COPY ./backend/src/rating_service /rating
COPY ./backend/config.yaml /rating
COPY ./backend/src/requirements.txt /rating

# Попробуем по одному (или 2-3 за раз) — для теста
RUN pip install --no-cache-dir -r requirements.txt --timeout 600 -v && echo "DONE installing" && sleep 5

EXPOSE 8050

CMD ["python3", "app/main.py"]
