from models.usuario import Usuario
class UsuarioRepository:
    def __init__(self, banco):
        self.banco = banco
    
    def salvar(self, usuario):
        conexao = self.banco.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
        INSERT INTO usuarios
        (nome, username, email, senha_hash, cep)
        VALUES
        (?, ?, ?, ?, ?)
    """, (
        usuario.nome,
        usuario.username,
        usuario.email,
        usuario.senha_hash,
        usuario.cep
    ))
        conexao.commit()
        conexao.close()
    
    def buscar_por_username(self, username):
        conexao = self.banco.conectar()
        cursor = conexao.cursor()
        cursor.execute(
        "SELECT * FROM usuarios WHERE username = ?",
        (username,)
    )
        resultado = cursor.fetchone()
        conexao.close()
        if resultado is None:
            return None
        return Usuario(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5])

    def buscar_por_email(self, email):
        conexao = self.banco.conectar()
        cursor = conexao.cursor()
        cursor.execute(
        "SELECT * FROM usuarios WHERE email = ?",
        (email,)
    )
        resultado = cursor.fetchone()
        conexao.close()
        if resultado is None:
            return None
        return Usuario(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5])



