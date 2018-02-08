from nameko.rpc import rpc
import sojobs.scraping

class ScrapeStackOverflowJobListingsMicroService:
    name = "stack_overflow_job_listings_scraping_microservice"

    @rpc
    def get_job_listing_info(self, job_listing_id):
        listing = sojobs.scraping.get_job_listing_info(job_listing_id)
        print(listing)
        return listing
