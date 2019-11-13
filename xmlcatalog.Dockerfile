FROM python:3.7.5

COPY ./xmlcatalog /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "huey_consumer.py", "service.huey" ]
