FROM python:3.10-slim-buster

WORKDIR /reservation

COPY ./backend/src/reservation_service /reservation
COPY ./backend/config.yaml /reservation
COPY ./backend/src/requirements.txt /reservation

# Попробуем по одному (или 2-3 за раз) — для теста
RUN pip install --no-cache-dir -r requirements.txt --timeout 600 -v && echo "DONE installing" && sleep 5

EXPOSE 8070

CMD ["python3", "app/main.py"]
