from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
import twisted.internet.defer

class ResponsePrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished

    def dataReceived(self, bytes):
        print('received {response_length}'.format(response_length=len(bytes)))

    def connectionLost(self, reason):
        print('Finished receiving body:', reason.getErrorMessage())
        self.finished.callback(None)


def getPage(url):
    print("Requesting %s" % (url,))
    agent = Agent(reactor)
    d = agent.request('GET', url, Headers({'User-Agent': ['Twisted Web Client']}), None)
    d.addCallback(cbRequest)
    return d

def cbRequest(response):
    print('Response version:', response.version)
    print('Response code:', response.code)
    finished = Deferred()
    response.deliverBody(ResponsePrinter(finished))
    return finished

def cbShutdown(ignored):
    reactor.stop()

semaphore = twisted.internet.defer.DeferredSemaphore(2)
dl = list()

dl.append(semaphore.run(getPage, 'http://www.google.com'))
dl.append(semaphore.run(getPage, 'http://www.google.com'))
dl.append(semaphore.run(getPage, 'http://www.google.com'))
dl.append(semaphore.run(getPage, 'http://www.google.com'))
dl = twisted.internet.defer.DeferredList(dl)
dl.addBoth(cbShutdown)

reactor.run()