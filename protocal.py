
from packet import *
from soc import *
from file import FileManager
import requests
import pickle
import time

DEFAULT_RECEIVE_SIZE = 100000
DEFAULT_SEND_DELAY = 0.1

server = None
client = None
fm = FileManager()

file_to_send = None
file_to_receive = None

def _split_data(data, size) :
    temp_data = ""
    data_list = []
    
    for i in range(len(data)) :
        if len((temp_data + data[i]).encode()) >= size :
            data_list.append(temp_data)

            temp_data = ""

        temp_data += data[i]

    return data_list

def _split_packet(middle_packet) :
    packet_size = len(pickle.dumps(middle_packet))

    if packet_size < DEFAULT_RECEIVE_SIZE :
        return None

    else :
        data_size = len(middle_packet.data.encode())
        header_size = packet_size - data_size
        
        data_list = _split_data(middle_packet.data, DEFAULT_RECEIVE_SIZE - header_size)
        packet_list = []

        for i in range(len(data_list)) :
            state = None
            
            if i == 0 :
                state = START_OF_FILE
            
            elif i == len(data_list) - 1 :
                state = END_OF_FILE

            else :
                state = MIDDLE_OF_FILE

            packet = MiddlePacket()
            packet.set_header(
                state,
                middle_packet.file_extension,
                middle_packet.file_size,
                middle_packet.file_name
            )
            packet.set_data(data_list[i])
            
            packet_list.append(packet)

        return packet_list

def _handshake(state) :
    handshake_packet = HandshakePacket()
    handshake_packet.set_header(
        requests.get("http://ip.jsontest.com").json()["ip"],
        state
    )

    if state == CONNECT_TO_SEND :
        server.send(pickle.dumps(handshake_packet))

    if state == CONNECT_TO_RECEIVE :
        client.send(pickle.dumps(handshake_packet))

    return handshake_packet

def _send(file_name) :
    middle_packet = MiddlePacket()
    file_info = fm.get_info(file_name)

    middle_packet.set_header(
        RECEIVE_NUMBER,
        file_info["file_extension"],
        file_info["file_size"],
        file_info["file_name"]
    )
    middle_packet.set_data(file_info["file_data"])

    packet_list = _split_packet(middle_packet)

    middle_packet.set_data(str(len(packet_list) if packet_list else 1).encode())

    if server :
        server.send(pickle.dumps(middle_packet))

    if client :
        client.send(pickle.dumps(middle_packet))

    if packet_list :
        for packet in packet_list :
            print(len(pickle.dumps(packet)))

            if server :
                server.send(pickle.dumps(packet))

            if client :
                client.send(pickle.dumps(packet))

            time.sleep(DEFAULT_SEND_DELAY)

        return packet_list

    else :
        middle_packet.set_header(
            END_OF_FILE,
            file_info["file_extension"],
            file_info["file_size"],
            file_info["file_name"]
        )
        middle_packet.set_data(file_info["file_data"])

        if server :
            server.send(pickle.dumps(middle_packet))

        if client :
            client.send(pickle.dumps(middle_packet))

        return middle_packet

def send(file_name) :
    global file_to_send

    file_to_send = file_name

def _receive() :
    if server :
        return pickle.loads(server.receive())

    if client :
        return pickle.loads(client.receive())

def receive() :
    global file_to_receive

    file_to_receive = file_name

def connect_server(host, port) :
    global server
    
    server = ServerSocket(host, port, DEFAULT_RECEIVE_SIZE)    
    server.listen()
    server.connect()

    _handshake(CONNECT_TO_SEND)

    handshake_packet = _receive()

    print(handshake_packet.sender_ip)

    _send(file_to_send)

def connect_client(host, port) :
    global client

    client = ClientSocket(host, port, DEFAULT_RECEIVE_SIZE)
    client.connect()

    handshake_packet = _receive()

    print(handshake_packet.sender_ip)

    _handshake(CONNECT_TO_RECEIVE)

    receive_number_packet = _receive()
    receive_number = int(receive_number_packet.data.decode())

    print(receive_number)

    for i in range(receive_number) :
        middle_packet = _receive()

        fm.append_data(
            middle_packet.file_name + "." + middle_packet.file_extension,
            middle_packet.data
        )
        
def close() :
    global server, client

    if server :
        server.close()

    if client :
        client.close()
