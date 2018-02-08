import requests
from bs4 import BeautifulSoup
from imdb.models import ImdbActorInfo
from urllib import parse
import os
from imdb.models import ImdbTitleInfo

def search_for_actor_return_search_result(actor_name):
    url_encoded_name = parse.urlencode({"q": actor_name})
    search_url = "http://www.imdb.com/find?ref_=nv_sr_fn&s=nm&%s" % url_encoded_name
    html = requests.get(search_url).text
    return html


def extract_actor_id_from_search_result(actor_search_result):
    soup = BeautifulSoup(actor_search_result, "lxml")
    row = soup.find("td", {"class": "result_text"})
    anchor = row.find("a")

    path = parse.urlparse(anchor["href"]).path
    return os.path.split(os.path.split(path)[0])[1]


def search_for_actor_id(actor_name):
    search_result_html = search_for_actor_return_search_result(actor_name)
    actor_id = extract_actor_id_from_search_result(search_result_html)
    return actor_id


def get_actor_page_html(actor_id):
    actor_url = "http://www.imdb.com/name/%s" % actor_id
    return requests.get(actor_url).text


def get_actor_info_from_actor_page_html(actor_page_html):
    soup = BeautifulSoup(actor_page_html, "lxml")
    meta_title = soup.find("meta", {"property": "og:title"})
    actor_name = meta_title["content"]
    meta_id = soup.find("meta", {"property": "pageId"})
    actor_id = meta_id["content"]

    actor_info = ImdbActorInfo(actor_name, actor_id, actor_page_html)

    titles = extract_acted_in_titles_from_actor_page_html(actor_info.html)
    actor_info.set_titles(titles)

    return actor_info


def get_actor_info_from_actor_id(actor_id):
    html = get_actor_page_html(actor_id)
    actor_info = get_actor_info_from_actor_page_html(html)
    return actor_info


def get_actor_info_from_actor_name(actor_name):
    actor_id = search_for_actor_id(actor_name)
    actor_info = get_actor_info_from_actor_id(actor_id)
    return actor_info


def get_title_page_html(title_id):
    title_url = "http://www.imdb.com/title/%s" % title_id
    return requests.get(title_url).text


def extract_acted_in_titles_from_actor_page_html(actor_page_html):
    soup = BeautifulSoup(actor_page_html, "lxml")
    filmo = soup.find("div", {"id": "filmography"})
    section = filmo.find("div", {"class": "filmo-category-section"})

    titles = []

    for row in section.find_all("div", {"class": "filmo-row"}):
        anchor = row.find("a")
        path = parse.urlparse(anchor["href"]).path
        id = os.path.split(os.path.split(path)[0])[1]
        title = anchor.text

        year = row.find("span", {"class": "year_column"}).text.strip()
        titles.append(ImdbTitleInfo(title, id, year))

    return titles


def get_actors_for_title(title_info):
    if title_info.html is None:
        title_info.html = get_title_page_html(title_info.id)
    actors = extract_actors_for_title_from_html(title_info.html)
    return actors


def extract_actors_for_title_from_html(title_page_html):
    soup = BeautifulSoup(title_page_html, "lxml")
    cast_list_table = soup.find("table", {"class": "cast_list"})
    actor_tds = cast_list_table.find_all("td", {"class": "itemprop", "itemprop": "actor"})

    actors = []

    for actor_td in actor_tds:
        anchor = actor_td.find("a")
        path = parse.urlparse(anchor["href"]).path
        actor_id = os.path.split(os.path.split(path)[0])[1]

        actor_span = anchor.find("span", {"class": "itemprop", "itemprop": "name"})
        actor_name = actor_span.text

        actors.append(ImdbActorInfo(actor_name, actor_id, None))

    return actors


def get_titles_for_actor(actor_info):
    titles = extract_acted_in_titles_from_actor_page_html(actor_page_html)
    return titles