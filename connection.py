from dataclasses import dataclass
import socket


@dataclass
class Connection:
    client_socket: socket.socket
    addr: str
    port: str
    id: str = None
