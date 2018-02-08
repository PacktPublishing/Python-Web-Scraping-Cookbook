from flask import Flask, request
from flask_restful import Resource, Api
from elasticsearch import Elasticsearch
from nameko.standalone.rpc import ClusterRpcProxy
import os, sys

app = Flask(__name__)
api = Api(app)

class JobListing(Resource):
    def get(self, job_listing_id):
        print("Request for job listing with id: " + job_listing_id)

        host = 'localhost'
        if os.environ.get('ES_HOST'):
            host = os.environ.get('ES_HOST')
        print("ElasticSearch host: " + host)

        es = Elasticsearch(hosts=[host])
        if (es.exists(index='joblistings', doc_type='job-listing', id=job_listing_id)):
            print('Found the document in ElasticSearch')
            doc =  es.get(index='joblistings', doc_type='job-listing', id=job_listing_id)
            return doc['_source']

        print('Not found in ElasticSearch, trying a scrape')

        CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}
        if os.environ.get('JOBS_AMQP_URL'):
            CONFIG['AMQP_URI'] = os.environ.get('JOBS_AMQP_URL')
        print("AMQP_URI: " + CONFIG["AMQP_URI"])

        with ClusterRpcProxy(CONFIG) as rpc:
            listing = rpc.stack_overflow_job_listings_scraping_microservice.get_job_listing_info(job_listing_id)
            print("Microservice returned with a result - storing in ElasticSearch")
            es.index(index='joblistings', doc_type='job-listing', id=job_listing_id, body=listing)
            return listing

api.add_resource(JobListing, '/', '/joblisting/<string:job_listing_id>')

class JobSearch(Resource):
    def post(self):
        skills = request.form['skills']
        print("Request for jobs with the following skills: " + skills)

        host = 'localhost'
        if os.environ.get('ES_HOST'):
            host = os.environ.get('ES_HOST')
        print("ElasticSearch host: " + host)

        es = Elasticsearch(hosts=[host])
        search_definition = {
            "query": {
                "match": {
                    "JSON.skills": {
                        "query": skills,
                        "operator": "AND"
                    }
                }
            },
            "_source": ["ID"]
        }

        try:
            result = es.search(index="joblistings", doc_type="job-listing", body=search_definition)
            print(result)
            return result

        except:
            return sys.exc_info()[0]

api.add_resource(JobSearch, '/', '/joblistings/search')

if __name__ == '__main__':
    print("Starting the job listing API ...")
    app.run(host='0.0.0.0', port=8080, debug=True)