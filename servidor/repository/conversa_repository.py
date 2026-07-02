from models.conversa import Conversa
class ConversaRepository:
    """
    Classe responsável por todas as operações de banco de dados
    relacionadas às conversas entre usuários.
    """
    def __init__(self, banco):
        # Instância do banco de dados (SQLite wrapper)
        self.banco = banco
    
    def criar_conversa(self, usuario1_id, usuario2_id):
        """
        Cria uma nova conversa entre dois usuários.
        Não verifica duplicidade aqui (isso deve ser feito no service).
        """
        conexao = self.banco.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
        INSERT INTO conversas
        (usuario1_id, usuario2_id)
        VALUES
        (?, ?)
        """, (
            usuario1_id,
            usuario2_id
        ))
        conexao.commit()
        conexao.close()
    
    def buscar_por_usuarios(self, usuario1_id, usuario2_id):
        """
        Busca uma conversa específica entre dois usuários,
        independente da ordem (A-B ou B-A).
        """
        conexao = self.banco.conectar()
        cursor = conexao.cursor()
        cursor.execute("""SELECT *
            FROM conversas
            WHERE
            (usuario1_id = ? AND usuario2_id = ?)
            OR
            (usuario1_id = ? AND usuario2_id = ?)
            """, (usuario1_id, usuario2_id, usuario2_id, usuario1_id))
        resultado = cursor.fetchone()
        conexao.close()
        
        # Se não existir conversa, retorna None
        if resultado is None:
            return None
        
        # Mapeia resultado do banco para objeto Conversa
        return Conversa(
            resultado[0],
            resultado[1],
            resultado[2]
            )

    def buscar_por_usuario(self, usuario_id):
        """
        Retorna todas as conversas de um usuário.
        (onde ele aparece como usuário1 ou usuário2)
        """
        conexao = self.banco.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM conversas
            WHERE usuario1_id = ?
            OR usuario2_id = ?
        """, (usuario_id, usuario_id))

        resultados = cursor.fetchall()

        conexao.close()

        conversas = []

        # Converte cada linha do banco em objeto Conversa
        for resultado in resultados:
            conversa = Conversa(
                resultado[0],  #id
                resultado[1],  #id_usuario1
                resultado[2]   #id_usuario2
            )

            conversas.append(conversa)

        return conversas
            