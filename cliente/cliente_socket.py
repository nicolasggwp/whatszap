import socket

cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

cliente.connect(
    ("127.0.0.1", 5000)
)

# Login
cliente.send(
    "LOGIN;nicolas;hash_teste".encode()
)

resposta = cliente.recv(1024)

print(
    "Servidor:",
    resposta.decode()
)

# Loop de testes
while True:
    mensagem = input("> ")

    if mensagem == "sair":
        break

    cliente.send(
        mensagem.encode()
    )

    try:
        resposta = cliente.recv(1024)

        if resposta:
            print(
                "Servidor:",
                resposta.decode()
            )
    except:
        pass

cliente.close()