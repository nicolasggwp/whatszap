from repository.usuario_repository import *
class AutenticacaoService:
    """
    Serviço responsável pela lógica de autenticação e registro de usuários.
    Aqui ficam as regras de negócio (não acesso direto ao banco).
    """
    def __init__(self, usuario_repository):
        # Repository responsável pelo acesso ao banco de usuários
        self.usuario_repository = usuario_repository
    
    def cadastrar_usuario(self, nome, username, email, senha_hash, cep):
        """
        Realiza o cadastro de um novo usuário.

        Regras:
        - Username deve ser único
        - Email deve ser único
        """
        
        # Verifica se já existe usuário com esse username
        usuario = self.usuario_repository.buscar_por_username(username)
        if usuario is not None:
            print("Username já existe")
            return False
        
        # Verifica se já existe usuário com esse email
        usuario = self.usuario_repository.buscar_por_email(email)
        if usuario is not None:
            print("Email já existe")
            return False
        
        # Cria objeto Usuario (ainda não salvo no banco)
        novo_usuario = Usuario(None, nome, username, email, senha_hash, cep)
        
        # Persiste no banco
        self.usuario_repository.salvar(novo_usuario)
        return True

    def fazer_login(self, username, senha_hash):
        """
        Realiza autenticação de usuário.

        Retorno:
        - Usuario (se login for válido)
        - False (se usuário não existir)
        - None (se senha estiver incorreta)
        """
        
        # Busca usuário pelo username
        usuario = self.usuario_repository.buscar_por_username(username)
        
        # Usuário não existe
        if not usuario:
            print("usuario nao existe")
            return False
        # Validação de senha
        if usuario.senha_hash != senha_hash:
            print("senha incorreta")
            return None
        
        # Login bem-sucedido
        return usuario