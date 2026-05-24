FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD sh -c "python src/backend/config/init_db.py && uvicorn src.backend.main:app --host 0.0.0.0 --port 8000"