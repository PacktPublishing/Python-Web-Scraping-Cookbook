import requests
from bs4 import BeautifulSoup
from urllib import parse
import os
from tmdb.models import ActorInfo, TitleInfo

def search_for_actor_return_search_result(actor_name):
    url_encoded_name = parse.urlencode({"query": actor_name})
    search_url = "https://www.themoviedb.org/search/person?%s" % url_encoded_name
    html = requests.get(search_url).text
    return html


def extract_actor_info_from_search_result(actor_search_result):
    soup = BeautifulSoup(actor_search_result, "lxml")
    anchor = soup.find("a", {"class": "result"})
    path = parse.urlparse(anchor["href"]).path
    id = os.path.split(path)[1]
    name = anchor["title"]
    return ActorInfo(name, id, None)


def extract_actor_id_from_search_result(actor_search_result):
    actor = extract_actor_info_from_search_result(actor_search_result)
    return actor.id


def get_actor_page_html(actor_id):
    actor_url = "http://www.themoviedb.org/person/%s" % actor_id
    response = requests.get(actor_url)
    html = response.text
    return html


def get_actor_info_from_actor_page_html(actor_page_html):
    soup = BeautifulSoup(actor_page_html, "lxml")
    name = soup.find("meta", property="og:title")["content"]
    id = soup.find("meta", property="og:url")["content"].split('/')[3].split('-')[0]
    actor = ActorInfo(name, id, actor_page_html)
    return actor


def get_actor_info_from_actor_id(actor_id):
    html = get_actor_page_html(actor_id)
    actor_info = get_actor_info_from_actor_page_html(html)
    return actor_info


def search_for_actor_id(actor_name):
    search_result_html = search_for_actor_return_search_result(actor_name)
    actor_id = extract_actor_id_from_search_result(search_result_html)
    return actor_id


def get_actor_info_from_actor_name(actor_name):
    actor_id = search_for_actor_id(actor_name)
    actor_info = get_actor_info_from_actor_id(actor_id)
    return actor_info


def extract_acted_in_titles_from_actor_page_html(actor_page_html):
    soup = BeautifulSoup(actor_page_html, "lxml")

    movie_spans = soup.find_all("span", {"data-type": "movie"})
    movie_trs = [span.parent.parent for span in movie_spans]
    movie_titles = [TitleInfo(
        tr.find("a", {"class": "tooltip"}).find("bdi").text,
        tr.find("span")["data-slug"],
        tr.find("td", {"class": "year"}).text
    ) for tr in movie_trs]
    return movie_titles


def get_title_page_html(title_id):
    title_url = "http://www.themoviedb.org/movie/%s" % title_id
    return requests.get(title_url).text


def get_cast_page_html(title_id):
    actor_url = "http://www.themoviedb.org/movie/%s/cast" % title_id
    response = requests.get(actor_url)
    html = response.text
    return html


def get_actors_for_title(title_info):
    if title_info.html is None:
        title_info.html = get_title_page_html(title_info.id)
    actors = extract_actors_from_title_cast_html(title_info.html)
    return actors


def extract_actors_from_title_cast_html(title_page_html):
    soup = BeautifulSoup(title_page_html, "lxml")

    people_credits = soup.find("ol", {"class": "people credits "})
    divs = people_credits.find_all("div", {"class": "info"})
    actor_anchors = [div.find("a") for div in divs]
    actors = [ActorInfo(
        actor.text,
        actor["href"].split('/')[2].split('-')[0],
        None
    ) for actor in actor_anchors]

    return actors


def get_titles_for_actor(actor_page_html):
    titles = extract_acted_in_titles_from_actor_page_html(actor_page_html)
    return titles