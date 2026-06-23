class Usuario:
    def __init__(self, id, nome, username, email, senha_hash, cep):
        self.id = id
        self.nome = nome
        self.username = username
        self.email = email
        self.senha_hash = senha_hash
        self.cep = cep