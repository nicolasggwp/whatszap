from banco.database import BancoDados
from repository.usuario_repository import UsuarioRepository
from models.usuario import Usuario
from services.autenticacao_service import *
from repository.conversa_repository import *
from repository.mensagem_repository import *
from models.mensagem import *
from services.conversa_service import ConversaService


banco = BancoDados()
repo = ConversaRepository(banco)

service = ConversaService(repo)

conversa = service.obter_ou_criar_conversa(1, 3)

print(conversa.id)
print(conversa.usuario1_id)
print(conversa.usuario2_id)