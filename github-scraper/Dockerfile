FROM alpine:latest

RUN apk update
RUN apk add python3 py3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

# Replace arguments with environment variables
CMD ["python3", "scraper.py", "PYTHON3", "8", "400", "True"]

