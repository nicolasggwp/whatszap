from threading import Thread
import socket

cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

cliente.connect(("127.0.0.1", 5000))


# -------- RECEBER MENSAGENS --------
def receber():
    while True:
        try:
            dados = cliente.recv(1024)

            if not dados:
                print("Servidor desconectou.")
                break

            print("\nServidor:", dados.decode())
            print("> ", end="")

        except:
            break


# -------- LOGIN --------
cliente.send("AUTH;;luck;hash123".encode())

resposta = cliente.recv(1024)
print("Servidor:", resposta.decode())


# -------- THREAD DE RECEBIMENTO --------
thread_receber = Thread(target=receber)
thread_receber.daemon = True
thread_receber.start()


# -------- LOOP DE ENVIO --------
while True:
    mensagem = input("> ")

    if mensagem == "sair":
        break

    cliente.send(f"CHAT;SEND;1;{mensagem}".encode())


cliente.close()
