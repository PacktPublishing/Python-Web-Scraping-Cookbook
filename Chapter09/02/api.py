from flask import Flask
from flask_restful import Resource, Api
from sojobs.scraping import get_job_listing_info

app = Flask(__name__)
api = Api(app)

class JobListing(Resource):
    def get(self, job_listing_id):
        print("Request for job listing with id: " + job_listing_id)
        listing = get_job_listing_info(job_listing_id)
        print("Got the following listing as a response: " + listing)
        return listing

api.add_resource(JobListing, '/', '/joblisting/<string:job_listing_id>')

if __name__ == '__main__':
    print("Starting the job listing API")
    app.run(debug=True)