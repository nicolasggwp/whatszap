from repository.mensagem_repository import *
class ClienteHandler:
    def __init__(self, cliente_socket, endereco, usuario_repository, conversa_service, mensagem_repository, usuarios_online):
        self.cliente_socket = cliente_socket
        self.endereco = endereco
        self.usuario_repository = usuario_repository
        self.usuarios_online = usuarios_online
        self.conversa_service = conversa_service
        self.mensagem_repository = mensagem_repository
        self.usuario = None

    def executar(self):
        print(f"Cliente conectado: {self.endereco}")

        while True:
            dados = self.cliente_socket.recv(1024)

            if not dados:
                break

            mensagem = dados.decode()
            partes = mensagem.split(";")
            comando = partes[0]
            if comando == "LOGIN":
                username = partes[1]
                senha = partes[2]

                usuario = self.usuario_repository.buscar_por_username(
                    username
                )

                if usuario is None:
                    print("Usuário não encontrado")

                    self.cliente_socket.send(
                        "LOGIN_ERRO".encode()
                    )

                    continue

                if usuario.senha_hash == senha:
                    print("Usuário encontrado")

                    self.cliente_socket.send(
                        "LOGIN_OK".encode()
                    )
                    self.usuario = usuario
                    self.usuarios_online[usuario.id] = self.cliente_socket
                    print(self.usuarios_online)
                else:
                    self.cliente_socket.send(
                        "LOGIN_ERRO".encode()
                    )
            
            elif comando == "MSG":
                destinatario_id = int(partes[1])
                texto = partes[2]
                destinatario = self.usuario_repository.buscar_por_id(
                destinatario_id)

                if destinatario is None:
                    self.cliente_socket.send(
                        "USUARIO_NAO_EXISTE".encode()
                    )
                    continue

                conversa = self.conversa_service.obter_ou_criar_conversa(self.usuario.id, destinatario_id)
                mensagem = Mensagem(None, conversa.id, self.usuario.id, texto)
                self.mensagem_repository.salvar(mensagem)
