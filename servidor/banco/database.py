import sqlite3
class BancoDados:
    def __init__(self, nome_banco="whatszap.db"):
        self.nome_banco = nome_banco

    def conectar(self):
        return sqlite3.connect(self.nome_banco)

    def criar_tabelas(self):
        conexao = self.conectar()
        cursor = conexao.cursor()
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
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario1_id INTEGER NOT NULL,
        usuario2_id INTEGER NOT NULL,
        FOREIGN KEY (usuario1_id) REFERENCES usuarios(id),
        FOREIGN KEY (usuario2_id) REFERENCES usuarios(id)
    )
    """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS mensagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversa_id INTEGER NOT NULL,
    remetente_id INTEGER NOT NULL,
    texto TEXT NOT NULL,
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversa_id) REFERENCES conversas(id),
    FOREIGN KEY (remetente_id) REFERENCES usuarios(id)
)""")
        conexao.commit()
        cursor.close()
        conexao.close()
    


   
