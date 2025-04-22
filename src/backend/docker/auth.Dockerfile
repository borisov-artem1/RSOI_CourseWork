FROM python:3.10-slim-buster

WORKDIR /auth

COPY ./backend/src/auth_service /auth
COPY ./backend/config.yaml /auth
COPY ./backend/src/requirements.txt /auth

# Попробуем по одному (или 2-3 за раз) — для теста
RUN pip install --no-cache-dir -r requirements.txt --timeout 600 -v && echo "DONE installing" && sleep 5

EXPOSE 8888

CMD ["python3", "app/main.py"]
