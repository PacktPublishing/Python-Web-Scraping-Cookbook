from elasticsearch import Elasticsearch
import requests
import json

if __name__ == '__main__':
    es = Elasticsearch(
        [
            "https://elastic:tduhdExunhEWPjSuH73O6yLS@7dc72d3327076cc4daf5528103c46a27.us-west-2.aws.found.io:9243"
        ])

    search_definition = {
        "query":{
            "match": {
                "hair_color": "blond"
            }
        }
    }

    result = es.search(index="sw", doc_type="people", body=search_definition)
    print(json.dumps(result, indent=4))