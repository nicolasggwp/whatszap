from repository.conversa_repository import *
class ConversaService:
    def __init__(self, conversa_repository):
        self.conversa_repository = conversa_repository
    
    def obter_ou_criar_conversa(self, usuario1_id, usuario2_id):
        conversa = self.conversa_repository.buscar_por_usuarios(usuario1_id, usuario2_id)
        if conversa:
            return conversa
        self.conversa_repository.criar_conversa(usuario1_id, usuario2_id)
        return self.conversa_repository.buscar_por_usuarios(usuario1_id, usuario2_id)