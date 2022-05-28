
import socket

class ServerSocket :
    def __init__(self, host, port, receive_size) :
        self.host = host
        self.port = port
        self.receive_size = receive_size

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self) :
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def connect(self) :
        self.client_socket, self.addr = self.socket.accept()

    def receive(self) :
        return self.client_socket.recv(self.receive_size)

    def send(self, data, socket) :
        return self.client_socket.send(data)

class ClientSocket(ServerSocket) :
    def connect(self) :
        self.socket.connect((self.host, self.port))

    def receive(self) :
        return self.socket.recv(self.receive_size)

    def send(self, data) :
        return self.socket.send(data)
