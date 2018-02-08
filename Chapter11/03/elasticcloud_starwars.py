from elasticsearch import Elasticsearch
import requests
import json

if __name__ == '__main__':
    es = Elasticsearch(
        [
            "https://elastic:tduhdExunhEWPjSuH73O6yLS@7dc72d3327076cc4daf5528103c46a27.us-west-2.aws.found.io:9243"
        ])

    i = 1
    while i<20:
        r = requests.get('http://swapi.co/api/people/' + str(i))
        if r.status_code is not 200:
            print("Got a " + str(r.status_code) + " so stopping")
            break
        j = json.loads(r.content)
        print(i, j['name'])
        es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
        i = i + 1