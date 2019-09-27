import socket


class SocketClient:
    def __init__(self):
        self.client = socket.socket()
        self.client.connect(
            ('192.168.11.236', 8888)
        )

    def get_client(self):
        return self.client

# sk = SocketClient()
# client = sk.get_client()