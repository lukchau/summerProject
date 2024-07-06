FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY mysecrets.py .
COPY tgbot.py .

CMD ["python", "tgbot.py"]
