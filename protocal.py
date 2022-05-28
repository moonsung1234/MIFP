
from .packet import *
from .socket import *
from .file import FileManager
import requests
import pickle
import time
import math
import sys
import os

DEFAULT_RECEIVE_SIZE = 100
DEFAULT_DELAY = 0.2

server = None
client = None
fm = FileManager()

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


def connect(host, port) :
    global server, client
    
    server = ServerSocket(host, port, DEFAULT_RECEIVE_SIZE)
    # client = ClientSocket(host, port, DEFAULT_RECEIVE_SIZE)
    
    server.listen() 

    while True :
        server.connect()

        time.sleep(DEFAULT_DELAY) 

def handshake(state) :
    handshake_packet = HandshakePacket()
    handshake_packet.set_header(
        requests.get("http://ip.jsontest.com").json()["ip"],
        state
    )

    if server :
        server.client_socket.send(pickle.dumps(handshake_packet))

    if client :
        client.socket.send(pickle.dumps(handshake_packet))

    return handshake_packet

def send(file_name) :
    middle_packet = MiddlePacket()
    file_info = fm.get_info(file_name)

    middle_packet.set_header(
        START_OF_FILE, # no meaning
        file_info["file_extension"],
        file_info["file_size"],
        file_info["file_name"]
    )

    packet_list = _split_packet(middle_packet)

    for packet in packet_list :
        if server :
            server.client_socket.send(pickle.dumps([packet]))

        if client :
            client.socket.send(pickle.dumps(packet))


