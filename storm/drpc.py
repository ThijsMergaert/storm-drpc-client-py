from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from repoze.lru import lru_cache
from DistributedRPC import Client
import json

class DRPCClient:
    def __init__(self, host, port=3772, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.connect()

    def connect(self):
        self.socket = TSocket.TSocket(self.host, self.port)
        if self.timeout:
            self.socket.setTimeout(self.timeout)
        self.transport = TTransport.TFramedTransport(self.socket)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.transport.open()
        self.client = Client(self.protocol)

    def execute(self, func, args):
        return json.loads(self.client.execute(func, args))

    def executeJSON(self, func, **kwargs):
        return self.execute(func, json.dumps(kwargs))

    def close(self):
        self.transport.close()


class DRPCLRUClient(DRPCClient):
    def __init__(self, host, port=3772, timeout=None, cache_size=10):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.connect()
        cache_size = 100
        self.cache = lru_cache(maxsize=cache_size)
        self.execute = self.cache(self.execute)
