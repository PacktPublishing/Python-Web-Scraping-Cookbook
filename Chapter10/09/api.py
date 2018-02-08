from flask import Flask
from flask_restful import Resource, Api
from elasticsearch import Elasticsearch
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
api = Api(app)

CONFIG = {'AMQP_URI': "amqp://guest:guest@rabbitmq"}

class JobListing(Resource):
    def get(self, job_listing_id):
        print("Request for job listing with id: " + job_listing_id)

        es = Elasticsearch(hosts=["elastic"])
        if (es.exists(index='joblistings', doc_type='job-listing', id=job_listing_id)):
            print('Found the document in ElasticSearch')
            doc =  es.get(index='joblistings', doc_type='job-listing', id=job_listing_id)
            return doc['_source']

        print('Not found in ElasticSearch, trying a scrape')
        with ClusterRpcProxy(CONFIG) as rpc:
            listing = rpc.stack_overflow_job_listings_scraping_microservice.get_job_listing_info(job_listing_id)
            print("Microservice returned with a result - storing in ElasticSearch")
            es.index(index='joblistings', doc_type='job-listing', id=job_listing_id, body=listing)
            return listing

api.add_resource(JobListing, '/', '/joblisting/<string:job_listing_id>')

if __name__ == '__main__':
    print("Starting the job listing API ...")
    app.run(host='0.0.0.0', port=8080, debug=True)