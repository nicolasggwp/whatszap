class Mensagem:
    def __init__(self, id, conversa_id, remetente_id, texto, data_envio=None):
        # atributos internos 
        self._id = id
        self._conversa_id = conversa_id
        self._remetente_id = remetente_id
        self._texto = texto
        self._data_envio = data_envio

    # GETTERS

    @property
    def id(self):
        """ID da mensagem"""
        return self._id

    @property
    def conversa_id(self):
        """ID da conversa à qual a mensagem pertence"""
        return self._conversa_id

    @property
    def remetente_id(self):
        """ID do usuário que enviou a mensagem"""
        return self._remetente_id

    @property
    def texto(self):
        """Conteúdo da mensagem"""
        return self._texto

    @property
    def data_envio(self):
        """Data/hora em que a mensagem foi enviada"""
        return self._data_envio

    # SETTERS

    @conversa_id.setter
    def conversa_id(self, value):
        self._conversa_id = value

    @remetente_id.setter
    def remetente_id(self, value):
        self._remetente_id = value

    @texto.setter
    def texto(self, value):
        self._texto = value

    @data_envio.setter
    def data_envio(self, value):
        self._data_envio = value