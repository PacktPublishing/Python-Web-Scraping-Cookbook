FROM python:3
WORKDIR /usr/src/app

RUN pip install Flask-RESTful Elasticsearch Nameko

COPY 11/11/scraper_api.py .

CMD ["python", "-u", "scraper_api.py"]