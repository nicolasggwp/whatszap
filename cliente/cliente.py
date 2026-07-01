import socket
class Cliente:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("127.0.0.1", 5000))

    def send(self, msg):
        self.socket.send(msg.encode())
    def recv(self):
        return self.socket.recv(1024).decode()