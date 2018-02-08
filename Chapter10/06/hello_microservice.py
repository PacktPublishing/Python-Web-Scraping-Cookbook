from nameko.rpc import rpc

class HelloMicroService:
    name = "hello_microservice"

    @rpc
    def hello(self, name):
        print('Received a request from: ' + name)
        return "Hello, {}!".format(name)