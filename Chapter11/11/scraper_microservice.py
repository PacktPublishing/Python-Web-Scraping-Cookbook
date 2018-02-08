import eventlet
from nameko.runners import ServiceRunner
eventlet.monkey_patch()

from nameko.rpc import rpc
import sojobs.scraping
import signal, time, errno, os, sys

class ScrapeStackOverflowJobListingsMicroService:
    name = "stack_overflow_job_listings_scraping_microservice"

    @rpc
    def get_job_listing_info(self, job_listing_id):
        listing = sojobs.scraping.get_job_listing_info(job_listing_id)
        print(listing)
        return listing

    @rpc
    def ping(self):
        return "pong"


if __name__ == "__main__":
    print("Starting scraper microservice")

    while True:
        try:
            print("Looking for config")
            CONFIG = {"AMQP_URI": "pyamqp://guest:guest@localhost"}
            environ_amqp_uri = os.environ.get("AMQP_URI")
            if environ_amqp_uri:
                CONFIG["AMQP_URI"] = environ_amqp_uri

            print("Using the following host address: " + CONFIG["AMQP_URI"])
            service_runner = ServiceRunner(CONFIG)
            service_runner.add_service(ScrapeStackOverflowJobListingsMicroService)
            runlet = eventlet.spawn(service_runner.wait)

            def shutdown(signum, frame):
                # signal handlers are run by the MAINLOOP and cannot use eventlet
                # primitives, so we have to call `stop` in a greenlet
                print("Received SIGTERM")
                eventlet.spawn_n(service_runner.stop)

            signal.signal(signal.SIGTERM, shutdown)

            print("Starting service")
            service_runner.start()
            print("Started service")

            try:
                runlet.wait()
            except OSError as exc:
                if exc.errno == errno.EINTR:
                    # this is the OSError(4) caused by the signalhandler.
                    # ignore and go back to waiting on the runner
                    continue
                raise
            except KeyboardInterrupt:
                print()  # looks nicer with the ^C e.g. bash prints in the terminal
                try:
                    service_runner.stop()
                except KeyboardInterrupt:
                    print()  # as above
                    service_runner.kill()
            else:
                # runlet.wait completed
                break

            print("Stopping service")
            service_runner.stop()
        except:
            print("Exception.  Pausing for a little and then retrying to start service")
            time.sleep(5)
