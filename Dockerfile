FROM python:3.12-slim

WORKDIR /backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
COPY backend backend/

EXPOSE $BACKEND_PORT

CMD uvicorn backend.main:app --host 0.0.0.0 --port $BACKEND_PORT
