from repository.usuario_repository import *
class AutenticacaoService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository
    
    def cadastrar_usuario(self, nome, username, email, senha_hash, cep):
        usuario = self.usuario_repository.buscar_por_username(username)
        if usuario is not None:
            print("Username já existe")
            return False
        
        usuario = self.usuario_repository.buscar_por_email(email)
        if usuario is not None:
            print("Email já existe")
            return False
        novo_usuario = Usuario(None, nome, username, email, senha_hash, cep)
        
        self.usuario_repository.salvar(novo_usuario)
        return True

    def fazer_login(self, username, senha_hash):
        usuario = self.usuario_repository.buscar_por_username(username)
        if not usuario:
            print("usuario nao existe")
            return False
        if usuario.senha_hash != senha_hash:
            print("senha incorreta")
            return None
        return usuario