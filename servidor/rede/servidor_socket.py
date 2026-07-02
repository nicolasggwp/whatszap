import socket
from threading import Thread
from rede.cliente_handler import ClienteHandler

class ServidorSocket:
    """
    Classe responsável por:
    - Criar o servidor TCP
    - Aceitar conexões de clientes
    - Criar uma thread para cada cliente conectado
    - Manter controle de usuários online
    """
    def __init__(self, usuario_repository, conversa_service, mensagem_repository, conversa_repository):
        # endereço local do servidor
        self.host = "127.0.0.1"
        # porta onde o servidor vai escutar conexões
        self.porta = 5000
        
        # dependências (injeção de repositórios/serviços)
        self.usuario_repository = usuario_repository
        self.conversa_service = conversa_service
        self.mensagem_repository = mensagem_repository
        self.conversa_repository = conversa_repository
        
        # dicionário de usuários online:
        # {user_id: socket}
        self.usuarios_online = {}
    
    # INICIALIZAÇÃO DO SERVIDOR
    def iniciar(self):
        """
        Cria o socket do servidor e começa a escutar conexões.
        Para cada cliente conectado, cria uma nova thread.
        """
        # cria socket TCP/IP
        servidor = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # associa host e porta
        servidor.bind((self.host, self.porta))
        
        # coloca servidor em modo de escuta
        servidor.listen()
        print("Servidor iniciado!")
        
        # loop infinito esperando clientes
        while True:
            # bloqueia até um cliente conectar
            cliente_socket, endereco = servidor.accept()

            # cria handler responsável por esse cliente
            handler = ClienteHandler(
                cliente_socket,
                endereco,
                self.usuario_repository,
                self.conversa_service,
                self.mensagem_repository,
                self.conversa_repository,
                self.usuarios_online
            )

            # cria thread para não travar servidor
            thread = Thread(
                target=handler.executar
            )

            # inicia execução do cliente
            thread.start()