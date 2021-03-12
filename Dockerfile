FROM python:3.9.2-alpine3.13

WORKDIR /code

COPY requirements.txt .
COPY .env .
COPY src/ .

RUN pip install -r requirements.txt
CMD ["python", "./main.py"]