FROM python:3.8

WORKDIR /app

COPY requirements.txt .
COPY mysecrets.py .
COPY tgbot.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tgbot.py"]