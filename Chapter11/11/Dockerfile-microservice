FROM python:3
WORKDIR /usr/src/app

RUN pip install nameko BeautifulSoup4 nltk lxml
RUN python -m nltk.downloader punkt -d /usr/share/nltk_data all

COPY 11/11/scraper_microservice.py .
COPY modules/sojobs sojobs

CMD ["python", "-u", "scraper_microservice.py"]