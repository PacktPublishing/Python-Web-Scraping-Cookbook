from sojobs.scraping import get_job_listing_info
from elasticsearch import Elasticsearch
import json

if __name__ == "__main__":

    es = Elasticsearch(
        [
            "https://elastic:tduhdExunhEWPjSuH73O6yLS@7dc72d3327076cc4daf5528103c46a27.us-west-2.aws.found.io:9243"
        ])

    job_ids = ["122517", "163854", "138222", "164641"]

    for job_id in job_ids:
        if not es.exists(index='joblistings', doc_type='job-listing', id=job_id):
            listing = get_job_listing_info(job_id)
            es.index(index='joblistings', doc_type='job-listing', id=job_id, body=listing)

    search_definition = {
        "query": {
            "match": {
                "JSON.skills": {
                    "query": "c# sql",
                    "operator": "AND"
                }
            }
        },
        "_source": ["ID"]
    }

    result = es.search(index="joblistings", doc_type="job-listing", body=search_definition)
    print(json.dumps(result, indent=4))