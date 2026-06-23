from rede.servidor_socket import ServidorSocket
from banco.database import *
from repository.usuario_repository import *

banco = BancoDados()

usuario_repository = UsuarioRepository(
    banco
)

servidor = ServidorSocket(
    usuario_repository
)

servidor.iniciar()