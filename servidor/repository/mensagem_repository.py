from models.mensagem import Mensagem
class MensagemRepository:
    """
    Responsável por persistir e recuperar mensagens do banco de dados.
    """
    def __init__(self, banco):
        # Instância do banco de dados (wrapper do SQLite)
        self.banco = banco
    
    def salvar(self, mensagem):
        """
        Salva uma nova mensagem no banco de dados.
        A data de envio é definida automaticamente pelo SQLite.
        """
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
        """
        Retorna todas as mensagens de uma conversa específica,
        ordenadas pela data de envio (do mais antigo ao mais recente).
        """
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

        # Converte cada linha do banco em objeto Mensagem
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