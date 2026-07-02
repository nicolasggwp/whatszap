class Conversa:
    def __init__(self, id, usuario1_id, usuario2_id):
        # atributos internos
        self._id = id
        self._usuario1_id = usuario1_id
        self._usuario2_id = usuario2_id

    # GETTERS

    @property
    def id(self):
        """Retorna o ID da conversa (somente leitura)"""
        return self._id

    @property
    def usuario1_id(self):
        """Retorna o ID do usuário 1 da conversa"""
        return self._usuario1_id

    @property
    def usuario2_id(self):
        """Retorna o ID do usuário 2 da conversa"""
        return self._usuario2_id

    # SETTERS

    @usuario1_id.setter
    def usuario1_id(self, value):
        """Define o ID do usuário 1"""
        self._usuario1_id = value

    @usuario2_id.setter
    def usuario2_id(self, value):
        """Define o ID do usuário 2"""
        self._usuario2_id = value