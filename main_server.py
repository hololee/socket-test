import socket
import traceback
from _thread import *
import time
import json
from connection import Connection

STATUS_INIT = 0
STATUS_READY = 1

connections = []

HOST = 'localhost'
PORT = 11111


def socket_connection(connection: Connection, connections: list):
    print('>> Connected by: ', connection.id)

    while 1:
        try:
            data = connection['client_socket'].recv(1024)

            if not data:
                print('>> Disconnected by ' + connection.id)
                break

            data = json.loads(data.decode())

            if data['type'] == 'init':
                connection.id = data['id']
                connection.status = STATUS_READY
                print(f'>> {data["id"]} is connected.')

            elif connection.status == STATUS_READY:
                print(f'@{data["user"]}: {data["message"]}')

                # if needed, send data to clients.

        except ConnectionResetError:
            print('>> Disconnected by ' + connection['id'])
            break

    if connection in connections:
        connections.remove(connection)
        print('>> Remove connection: ', connection.id)

    connection['socket'].close()


def check_connection(server_socket):
    try:
        while True:
            print('>> Wait')

            client_socket, addr = server_socket.accept()
            connection = Connection(client_socket=client_socket, addr=addr[0], port=addr[1])

            # 관리 리스트에 추가.
            connections.append(connection)

            # 프로세스 시작.
            start_new_thread(socket_connection, (connection,))

    except Exception:
        traceback.print_exc()

    finally:
        server_socket.close()


# 서버 소켓 생성
print('>> Server Start')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()


start_new_thread(check_connection, (server_socket,))

while True:
    message = input('')
    if message == 'q':
        close_data = message
        break

    for connection in connections:
        connection.socket.send(message.encode())
