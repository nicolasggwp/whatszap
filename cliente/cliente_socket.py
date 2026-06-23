import socket

cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

cliente.connect(
    ("127.0.0.1", 5000)
)

cliente.send(
    "LOGIN;nicolas;hash_teste".encode()
)

resposta = cliente.recv(1024)

print(
    resposta.decode()
)