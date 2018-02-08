from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class JobListing(Resource):
    def get(self, job_listing_id):
        print("Request for job listing with id: " + job_listing_id)
        return {'YouRequestedJobWithId': job_listing_id}

api.add_resource(JobListing, '/', '/joblisting/<string:job_listing_id>')

if __name__ == '__main__':
    print("Starting the job listing API")
    app.run(debug=True)