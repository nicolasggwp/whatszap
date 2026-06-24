from rede.servidor_socket import ServidorSocket
from banco.database import *
from repository.usuario_repository import *
from repository.mensagem_repository import *
from repository.conversa_repository import *
from services.conversa_service import *

banco = BancoDados()

usuario_repository = UsuarioRepository(
    banco
)
mensagem_repository = MensagemRepository(banco)
conversa_repository = ConversaRepository(banco)

conversa_service = ConversaService(
    conversa_repository
)

servidor = ServidorSocket(
    usuario_repository, conversa_service,
    mensagem_repository
)

servidor.iniciar()