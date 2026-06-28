from models.conversa import Conversa
class ConversaRepository:
    def __init__(self, banco):
        self.banco = banco
    
    def criar_conversa(self, usuario1_id, usuario2_id):
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
        if resultado is None:
            return None
        return Conversa(
            resultado[0],
            resultado[1],
            resultado[2]
            )

    def buscar_por_usuario(self, usuario_id):
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

        for resultado in resultados:
            conversa = Conversa(
                resultado[0],  
                resultado[1],  
                resultado[2]   
            )

            conversas.append(conversa)

        return conversas
            