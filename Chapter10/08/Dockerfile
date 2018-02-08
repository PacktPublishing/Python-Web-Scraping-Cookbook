FROM python:3
WORKDIR /usr/src/app

RUN pip install nameko BeautifulSoup4 nltk lxml
RUN python -m nltk.downloader punkt -d /usr/share/nltk_data all

COPY 10/07/scraper_microservice.py .
COPY modules/sojobs sojobs

CMD ["nameko", "run", "--broker", "amqp://guest:guest@rabbitmq", "scraper_microservice"]