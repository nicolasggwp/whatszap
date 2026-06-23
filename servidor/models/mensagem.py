class Mensagem:
    def __init__(self, id, conversa_id, remetente_id, texto, data_envio=None):
        self.conversa_id = conversa_id
        self.remetente_id = remetente_id
        self.texto = texto
        self.data_envio = data_envio
        