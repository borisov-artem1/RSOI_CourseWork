FROM python:3.10-slim-buster

WORKDIR /gateway

COPY ./backend/src/gateway_service /gateway
COPY ./backend/config.yaml /gateway
COPY ./backend/src/requirements.txt /gateway

# Попробуем по одному (или 2-3 за раз) — для теста
RUN pip install --no-cache-dir -r requirements.txt --timeout 600 -v && echo "DONE installing" && sleep 5

EXPOSE 8080

CMD ["python3", "app/main.py"]
