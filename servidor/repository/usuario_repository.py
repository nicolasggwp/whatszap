from models.usuario import Usuario
class UsuarioRepository:
    """
    Responsável por todas as operações de persistência da entidade Usuario.
    Faz comunicação direta com o SQLite.
    """
    def __init__(self, banco):
        # Instância do banco de dados (classe que gerencia conexão SQLite)
        self.banco = banco
    
    def salvar(self, usuario):
        """
        Insere um novo usuário no banco de dados.
        """
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
        """
        Busca um usuário pelo username (login).
        Retorna um objeto Usuario ou None.
        """
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
        """
        Busca usuário pelo email.
        """
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
    
    def buscar_por_id(self, id):
        """
        Busca usuário pelo ID.
        Muito usado em relações entre tabelas (chat, mensagens, etc).
        """
        conexao = self.banco.conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE id = ?",
            (id,)
        )
        resultado = cursor.fetchone()
        conexao.close()
        if resultado is None:
            return None
        return Usuario(
            resultado[0],
            resultado[1],
            resultado[2],
            resultado[3],
            resultado[4],
            resultado[5]
        )

    def atualizar(self, usuario):
        """
        Atualiza dados editáveis do usuário.
        (nome, email e cep)
        """
        conexao = self.banco.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE usuarios
            SET nome = ?, email = ?, cep = ?
            WHERE id = ?
        """, (
            usuario.nome,
            usuario.email,
            usuario.cep,
            usuario.id
        ))

        conexao.commit()
        conexao.close()
    
    def remover(self, usuario_id):
        """
        Remove um usuário do banco de dados permanentemente.
        """
        conexao = self.banco.conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM usuarios WHERE id = ?",
            (usuario_id,)
        )

        conexao.commit()
        conexao.close()

