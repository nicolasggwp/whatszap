from repository.conversa_repository import *
class ConversaService:
    """
    Serviço responsável pela regra de negócio relacionada às conversas.

    Responsabilidade:
    - Garantir que não existam conversas duplicadas
    - Criar conversa apenas quando necessário
    - Retornar sempre uma conversa válida entre dois usuários
    """
    def __init__(self, conversa_repository):
        # Repository responsável pelo acesso ao banco de conversas
        self.conversa_repository = conversa_repository
    
    def obter_ou_criar_conversa(self, usuario1_id, usuario2_id):
        """
        Retorna uma conversa existente entre dois usuários.
        Caso não exista, cria uma nova conversa e retorna ela.

        Isso garante que sempre haverá apenas UMA conversa
        entre o mesmo par de usuários.
        """

        # 1. Verifica se já existe conversa entre os dois usuários
        conversa = self.conversa_repository.buscar_por_usuarios(usuario1_id, usuario2_id)
        
        # 2. Se já existir, retorna direto (evita duplicação)
        if conversa:
            return conversa
        
        # 3. Se não existir, cria nova conversa
        self.conversa_repository.criar_conversa(usuario1_id, usuario2_id)
        
        # 4. Busca novamente para retornar o objeto completo
        return self.conversa_repository.buscar_por_usuarios(usuario1_id, usuario2_id)