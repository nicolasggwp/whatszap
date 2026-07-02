import sqlite3
class BancoDados:
    def __init__(self, nome_banco="whatszap.db"):
        # Nome do arquivo do banco SQLite
        self.nome_banco = nome_banco

    def conectar(self):
        # Abre uma conexão com o banco de dados
        # Cada chamada cria uma nova conexão SQLite
        return sqlite3.connect(self.nome_banco)

    def criar_tabelas(self):
        # Cria todas as tabelas necessárias caso ainda não existam
        conexao = self.conectar()
        cursor = conexao.cursor()
        #tebela usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        cep TEXT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
        #tabela conversas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario1_id INTEGER NOT NULL,
        usuario2_id INTEGER NOT NULL,
        FOREIGN KEY (usuario1_id) REFERENCES usuarios(id),
        FOREIGN KEY (usuario2_id) REFERENCES usuarios(id)
    )
    """)
        #tabela mensagens
        cursor.execute("""CREATE TABLE IF NOT EXISTS mensagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversa_id INTEGER NOT NULL,
    remetente_id INTEGER NOT NULL,
    texto TEXT NOT NULL,
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversa_id) REFERENCES conversas(id),
    FOREIGN KEY (remetente_id) REFERENCES usuarios(id)
)""")
        # salva alterações no banco
        conexao.commit()
        
        # fecha recursos
        cursor.close()
        conexao.close()
    


   
