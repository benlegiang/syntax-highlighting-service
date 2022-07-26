FROM python:3.9.7-alpine3.14

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "localhost:8082", "app.main:app"]

