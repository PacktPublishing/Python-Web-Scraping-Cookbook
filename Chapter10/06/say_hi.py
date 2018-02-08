from nameko.standalone.rpc import ClusterRpcProxy

CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}

with ClusterRpcProxy(CONFIG) as rpc:
    result = rpc.hello_microservice.hello("Micro-service Client")
    print(result)
