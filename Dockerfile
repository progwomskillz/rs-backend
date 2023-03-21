FROM python:3.11.2-alpine3.17

RUN mkdir /app
WORKDIR /app

EXPOSE 8000

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT gunicorn -w 4 -b:8000 --access-logfile - scripts.run:application
