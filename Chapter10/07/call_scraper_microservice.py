from nameko.standalone.rpc import ClusterRpcProxy

CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}

with ClusterRpcProxy(CONFIG) as rpc:
    result = rpc.stack_overflow_job_listings_scraping_microservice.get_job_listing_info("122517")
    print(result)
