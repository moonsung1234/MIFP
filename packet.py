
HANDSHAKE_PACKET = 0
MIDDLE_PACKET = 1
INTERRUPT_PACKET = 2

CONNECT_TO_SEND = 10
CONNECT_TO_RECEIVE = 11

RECEIVE_NUMBER = 20
START_OF_FILE = 21
MIDDLE_OF_FILE = 22
END_OF_FILE = 23

class HandshakePacket :
    def __init__(self) :
        self.packet = HANDSHAKE_PACKET

    def set_header(self, sender_ip, state) :
        self.sender_ip = sender_ip
        self.state = state

    def set_data(self, data) :
        self.data = data

class MiddlePacket :
    def __init__(self) :
        self.packet = MIDDLE_PACKET

    def set_header(self, state, file_extension, file_size, file_name) :
        self.state = state
        self.file_extension = file_extension
        self.file_size = file_size
        self.file_name = file_name

    def set_data(self, data) :
        self.data = data

class InterruptPacket :
    def __init__(self) :
        self.packet = INTERRUPT_PACKET