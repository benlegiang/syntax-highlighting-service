FROM python:3.9.7-slim

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.main:app"]
# CMD ["gunicorn", "-w=4", "-b", "0.0.0.0:8000", "app.main:app"]

