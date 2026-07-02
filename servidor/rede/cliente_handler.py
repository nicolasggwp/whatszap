from repository.mensagem_repository import *
from repository.conversa_repository import *
from repository.usuario_repository import *
import bcrypt
import re
import requests

# VALIDAÇÃO DE SENHA FORTE
def senha_forte(senha):
    """
    Valida se a senha atende critérios mínimos de segurança:
    - mínimo 8 caracteres
    - pelo menos 1 letra maiúscula
    - pelo menos 1 letra minúscula
    - pelo menos 1 número
    - pelo menos 1 caractere especial
    """
    return (
        len(senha) >= 8 and
        re.search(r"[A-Z]", senha) and
        re.search(r"[a-z]", senha) and
        re.search(r"\d", senha) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha)
    )

class ClienteHandler:
    """
    Classe responsável por:
    - Receber mensagens do cliente via socket
    - Interpretar comandos (AUTH, CHAT, USER)
    - Interagir com banco/repositórios
    - Enviar respostas ao cliente
    """
    def __init__(self, cliente_socket, endereco, usuario_repository, conversa_service, mensagem_repository, conversa_repository, usuarios_online):
        # conexão com cliente
        self.cliente_socket = cliente_socket
        # endereço do cliente (IP/porta)
        self.endereco = endereco
        
        # repositórios e serviços do sistema
        self.usuario_repository = usuario_repository
        self.conversa_service = conversa_service
        self.mensagem_repository = mensagem_repository
        self.conversa_repository = conversa_repository
        
        # controle de usuários logados
        self.usuarios_online = usuarios_online
        # usuário autenticado nesta conexão (inicialmente nenhum)
        self.usuario = None

    # LOOP PRINCIPAL DO CLIENTE
    def executar(self):
        """
        Loop principal que:
        - recebe mensagens do cliente
        - interpreta protocolo
        - executa ações correspondentes
        """
        print(f"Cliente conectado: {self.endereco}")
        while True:
            dados = self.cliente_socket.recv(1024)

            # se não recebeu dados → cliente desconectou
            if not dados:
                break

            # decodifica mensagem recebida
            mensagem = dados.decode()
            print(mensagem)
            
            # separa protocolo
            partes = mensagem.split(";")
            categoria = partes[0]
            acao = partes[1]
            
            # LOGIN
            if categoria == "AUTH" and acao == "LOGIN":
                username = partes[2]
                senha = partes[3]

                usuario = self.usuario_repository.buscar_por_username(
                    username
                )

                if usuario is None:
                    print("Usuário não encontrado")

                    self.cliente_socket.send(
                        "LOGIN_ERRO\n".encode()
                    )

                    continue

                # valida senha hash
                if bcrypt.checkpw(
                    senha.encode(),
                    usuario.senha_hash.encode()
                ):
                    print("Usuário encontrado")
                    self.usuario = usuario
                    
                    # envia dados do usuário autenticado
                    self.cliente_socket.send(
                        f"AUTH;SUCCESS;LOGIN_OK;{self.usuario.id};{self.usuario.nome};{self.usuario.username};{self.usuario.email};{self.usuario.cep}\n".encode()
                    )
                   
                    # marca usuário como online
                    self.usuarios_online[usuario.id] = self.cliente_socket
                    print(self.usuarios_online)
                    continue
                else:
                    self.cliente_socket.send(
                        "CTRL;ERROR;LOGIN_ERRO\n".encode()
                    )

            # REGISTRO
            elif categoria == "AUTH" and acao == "REGISTER":
                nome = partes[2]
                username = partes[3]
                email = partes[4]
                senha = partes[5]
                cep = partes[6]

                # valida senha forte
                if not senha_forte(senha):
                    self.cliente_socket.send(
                        "CTRL;ERROR;WEAK_PASSWORD\n".encode()
                    )
                    continue

                # verifica duplicidade
                if self.usuario_repository.buscar_por_username(username) is not None:
                    self.cliente_socket.send(
                        "CTRL;ERROR;USERNAME_EXISTS\n".encode())
                    continue
                if self.usuario_repository.buscar_por_email(email) is not None:
                    self.cliente_socket.send(
                        "CTRL;ERROR;EMAIL_EXISTS\n".encode()
                    )
                    continue

                # valida CEP via API externa
                resposta = requests.get(
                f"https://viacep.com.br/ws/{cep}/json/")

                dados = resposta.json()

                if "erro" in dados:
                    self.cliente_socket.send(
                        "CTRL;ERROR;INVALID_CEP\n".encode()
                    )
                    continue

                # gera hash da senha
                senha_hash = bcrypt.hashpw(
                    senha.encode(),
                    bcrypt.gensalt()
                ).decode()

                # cria usuário
                usuario = Usuario(
                    None,
                    nome,
                    username,
                    email,
                    senha_hash,
                    cep
                )
                self.usuario_repository.salvar(usuario)
                self.cliente_socket.send("CTRL;OK;REGISTER\n".encode())
                self.cliente_socket.send("CTRL;OK;REGISTER\n".encode()
                )
                continue

            # BLOQUEIO CASO NÃO LOGADO
            elif self.usuario is None:
                self.cliente_socket.send("CTRL;ERROR;NOT_AUTHENTICATED\n")
                continue
            
            # ENVIAR MENSAGEM
            elif categoria == "CHAT" and acao == "SEND":
                destinatario_id = int(partes[2])
                texto = ";".join(partes[3:])
                destinatario = self.usuario_repository.buscar_por_id(
                destinatario_id)

                if destinatario is None:
                    self.cliente_socket.send(
                        "CTRL;ERROR;USUARIO_NAO_EXISTE\n".encode()
                    )
                    continue

                # cria ou obtém conversa
                conversa = self.conversa_service.obter_ou_criar_conversa(self.usuario.id, destinatario_id)
                
                # salva mensagem no banco
                mensagem = Mensagem(None, conversa.id, self.usuario.id, texto)
                self.mensagem_repository.salvar(mensagem)
                
                # envia mensagem em tempo real se destinatário estiver online
                socket_destino = self.usuarios_online.get(destinatario_id)
                if socket_destino is not None:
                    socket_destino.send(f"MSG;RECEIVE;{self.usuario.id};{texto}\n".encode())
            
            # LISTAR CONVERSAS
            elif categoria == "CHAT" and acao == "LIST":
                print("oiiii")
                conversas = self.conversa_repository.buscar_por_usuario(self.usuario.id)
                for conversa in conversas:
                    if conversa.usuario1_id == self.usuario.id:
                        outro_id = conversa.usuario2_id
                    else:
                        outro_id = conversa.usuario1_id

                    outro_usuario = self.usuario_repository.buscar_por_id(outro_id)
                    self.cliente_socket.send(f"CHAT;CONVERSA;{outro_usuario.id};{outro_usuario.username}\n".encode())
                self.cliente_socket.send("CHAT;LIST_END\n".encode())

            # ABRIR CONVERSA + HISTÓRICO
            elif categoria == "CHAT" and acao == "OPEN":
                destinatario_id = int(partes[2])

                destinatario = self.usuario_repository.buscar_por_id(destinatario_id)

                if destinatario is None:
                    self.cliente_socket.send("CTRL;ERROR;USER_NOT_FOUND\n".encode())
                    continue

                if destinatario.id == self.usuario.id:
                    self.cliente_socket.send("CTRL;ERROR;SELF_CHAT\n".encode())
                    continue

                conversa = self.conversa_service.obter_ou_criar_conversa(
                    self.usuario.id,
                    destinatario.id
                )

                mensagens = self.mensagem_repository.listar_por_conversa(conversa.id)

                for mensagem in mensagens:
                    self.cliente_socket.send(
                        f"CHAT;HISTORY;{mensagem.remetente_id};{mensagem.texto}\n".encode()
                    )

                self.cliente_socket.send("CHAT;HISTORY_END\n".encode())
                        
            # ATUALIZAR USUÁRIO
            elif categoria == "USER" and acao == "UPDATE":
                nome = partes[2]
                email = partes[3]
                cep = partes[4]

                self.usuario.nome = nome
                self.usuario.email = email
                self.usuario.cep = cep

                self.usuario_repository.atualizar(self.usuario)

                self.cliente_socket.send(
                    "USER;UPDATE_OK\n".encode()
                )
            
            # DELETAR CONTA
            elif categoria == "USER" and acao == "DELETE":
                self.usuario_repository.remover(self.usuario.id)

                self.cliente_socket.send(
                    "USER;DELETE_OK\n".encode()
                )

                self.cliente_socket.close()
                break

            elif categoria == "USER" and acao == "FIND":
                username = partes[2]

                usuario = self.usuario_repository.buscar_por_username(username)

                if usuario is None:
                    self.cliente_socket.send("USER;NOT_FOUND\n".encode())
                    continue

                self.cliente_socket.send(
                    f"USER;FOUND;{usuario.id};{usuario.username}\n".encode()
                )
            
        # LIMPEZA FINAL
        if self.usuario is not None:
            self.usuarios_online.pop(
                self.usuario.id,
                None
            )

        self.cliente_socket.close()
