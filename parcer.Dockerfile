FROM python:3.9-slim

RUN pip install requests
RUN pip install python-dotenv
RUN pip install psycopg2-binary

COPY parcer.py /app/
COPY database.py /app/

ENV USER_AGENT=${USER_AGENT}

WORKDIR /app/

CMD ["python", "parcer.py"]