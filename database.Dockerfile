FROM python:3.9-slim

WORKDIR /app/

RUN pip install psycopg2-binary
RUN pip install python-dotenv

COPY database.py .

ENV DATABASE_PASSWORD=${DATABASE_PASSWORD}

CMD ["python", "database.py"]