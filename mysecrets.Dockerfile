FROM python:3.9

WORKDIR /app

COPY mysecrets.py .

CMD ["python", "-m", "mysecrets"]