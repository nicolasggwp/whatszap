import socket
from threading import Thread
from rede.cliente_handler import ClienteHandler

class ServidorSocket:
    def __init__(self, usuario_repository, conversa_service, mensagem_repository, conversa_repository):
        self.host = "127.0.0.1"
        self.porta = 5000
        self.usuario_repository = usuario_repository
        self.conversa_service = conversa_service
        self.mensagem_repository = mensagem_repository
        self.conversa_repository = conversa_repository
        self.usuarios_online = {}
    
    def iniciar(self):
        servidor = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        servidor.bind((self.host, self.porta))
        servidor.listen()
        print("Servidor iniciado!")
        while True:
            cliente_socket, endereco = servidor.accept()

            handler = ClienteHandler(
                cliente_socket,
                endereco,
                self.usuario_repository,
                self.conversa_service,
                self.mensagem_repository,
                self.conversa_repository,
                self.usuarios_online
            )

            thread = Thread(
                target=handler.executar
            )

            thread.start()