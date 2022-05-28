
from .protocal import *

class FileOnline :
    def __init__(self, host, port) :
        self.host = host
        self.port = port

    def send(self, file_name) :
        send(file_name)
        connect_server(self.host, self.port)

    def receive(self, file_name) :
        receive(file_name)
        connect_client(self.host, self.port)

    def close(self) :
        close()