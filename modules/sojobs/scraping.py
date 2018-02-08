from bs4 import BeautifulSoup
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sojobs.tech2grams import tech_2grams
from sojobs.punctuation import remove_punctuation
import requests

def get_job_listing_info(job_listing_id):
    print("Got a request for a job listing with id: " + job_listing_id)

    req = requests.get("https://stackoverflow.com/jobs/" + job_listing_id)
    content = req.text

    bs = BeautifulSoup(content, "lxml")
    script_tag = bs.find("script", {"type": "application/ld+json"})

    job_listing_contents = json.loads(script_tag.contents[0])
    desc_bs = BeautifulSoup(job_listing_contents["description"], "lxml")
    just_text = desc_bs.find_all(text=True)

    joined = ' '.join(just_text)
    tokens = word_tokenize(joined)

    stop_list = stopwords.words('english')
    with_no_stops = [word for word in tokens if word.lower() not in stop_list]
    two_grammed = tech_2grams(with_no_stops)
    cleaned = remove_punctuation(two_grammed)

    result = {
        "ID": job_listing_id,
        "JSON": job_listing_contents,
        "TextOnly": just_text,
        "CleanedWords": cleaned
    }

    return json.dumps(result)

def get_job_listing_skills(job_listing_id):
    print("Got a request for a job listing skills with id: " + job_listing_id)

    req = requests.get("https://stackoverflow.com/jobs/" + job_listing_id)
    content = req.text

    bs = BeautifulSoup(content, "lxml")
    script_tag = bs.find("script", {"type": "application/ld+json"})

    job_listing_contents = json.loads(script_tag.contents[0])
    skills = job_listing_contents['skills']

    return json.dumps(skills)