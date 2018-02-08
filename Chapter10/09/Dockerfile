FROM python:3
WORKDIR /usr/src/app

RUN pip install Flask-RESTful Elasticsearch Nameko

COPY 10/09/api.py .

CMD ["python", "api.py"]