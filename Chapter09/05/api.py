from flask import Flask
from flask_restful import Resource, Api
from sojobs.scraping import get_job_listing_info
from sojobs.scraping import get_job_listing_skills
from elasticsearch import Elasticsearch

app = Flask(__name__)
api = Api(app)

class JobListing(Resource):
    def get(self, job_listing_id):
        print("Request for job listing with id: " + job_listing_id)

        es = Elasticsearch()
        if (es.exists(index='joblistings', doc_type='job-listing', id=job_listing_id)):
            print('Found the document in ElasticSearch')
            doc =  es.get(index='joblistings', doc_type='job-listing', id=job_listing_id)
            print(type(doc))
            return doc['_source']

        listing = get_job_listing_info(job_listing_id)
        es.index(index='joblistings', doc_type='job-listing', id=job_listing_id, body=listing)

        print("Got the following listing as a response: " + listing)
        return listing

api.add_resource(JobListing, '/', '/joblisting/<string:job_listing_id>')

class JobListingSkills(Resource):
    def get(self, job_listing_id):
        print("Request for job listing's skills with id: " + job_listing_id)

        es = Elasticsearch()
        if (es.exists(index='joblistings', doc_type='job-listing', id=job_listing_id)):
            print('Found the document in ElasticSearch')
            doc =  es.get(index='joblistings', doc_type='job-listing', id=job_listing_id)
            return doc['_source']['JSON']['skills']

        skills = get_job_listing_skills(job_listing_id)

        print("Got the following skills as a response: " + skills)
        return skills

api.add_resource(JobListingSkills, '/', '/joblisting/<string:job_listing_id>/skills')

if __name__ == '__main__':
    print("Starting the job listing API")
    app.run(debug=True)