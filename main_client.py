import socket
import json
import time
from _thread import *

HOST = 'localhost'
PORT = 11111

is_inferencing = False

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def load_next():
    # implement get data.
    data = {'id': '10001', 'data': 'payload'}
    client_socket.send(json.dumps({'type': 'init', 'id': data['id']}).encode())

    return data


def inference(data):
    for i in range(100):
        time.sleep(1)


def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        if data:
            return data


start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')


while True:
    # load next data from server queue.
    data = load_next()
    recv_data(client_socket)
    is_inferencing = True
    inference(data)
    client_socket.send(json.dumps({'type': 'message', 'message': 'fin', 'id': 'task1'}).encode())
    is_inferencing = False


client_socket.close()
