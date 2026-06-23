from models.mensagem import Mensagem
class MensagemRepository:
    def __init__(self, banco):
        self.banco = banco
    
    def salvar(self, mensagem):
        conexao = self.banco.conectar()
        cursor = conexao.cursor()
        cursor.execute("""INSERT INTO mensagens
        (conversa_id, remetente_id, texto)
        VALUES
        (?, ?, ?)""",
        (
        mensagem.conversa_id,
        mensagem.remetente_id,
        mensagem.texto
        ))
        conexao.commit()
        conexao.close()

    def listar_por_conversa(self, conversa_id):
        conexao = self.banco.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT *
        FROM mensagens
        WHERE conversa_id = ?
        ORDER BY data_envio
        """, (conversa_id,))
        resultados = cursor.fetchall()
        mensagens = []

        for resultado in resultados:
            mensagem = Mensagem(
                resultado[0],
                resultado[1],
                resultado[2],
                resultado[3],
                resultado[4]
                )

            mensagens.append(mensagem)
        conexao.close()
        return mensagens