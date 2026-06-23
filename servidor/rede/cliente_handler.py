class ClienteHandler:
    def __init__(self, cliente_socket, endereco, usuario_repository):
        self.cliente_socket = cliente_socket
        self.endereco = endereco
        self.usuario_repository = usuario_repository
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
                else:
                    self.cliente_socket.send(
                        "LOGIN_ERRO".encode()
                    )