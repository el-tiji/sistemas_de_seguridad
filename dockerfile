FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn sqlalchemy pymysql python-multipart passlib[bcrypt] itsdangerous

CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]