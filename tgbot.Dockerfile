FROM python:3.9-slim

RUN pip install python-telegram-bot
RUN pip install pyTelegramBotAPI
RUN pip install psycopg2-binary
RUN pip install python-dotenv

COPY tgbot.py /app/
COPY parcer.py /app/
COPY database.py /app/

ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}

WORKDIR /app/

CMD ["python", "tgbot.py"]