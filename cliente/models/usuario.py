class Usuario:
    def __init__(self, id, nome, username, email, senha_hash, cep):
        # atributos internos
        self._id = id
        self._nome = nome
        self._username = username
        self._email = email
        self._senha_hash = senha_hash
        self._cep = cep

    # GETTERS

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def senha_hash(self):
        return self._senha_hash

    @property
    def cep(self):
        return self._cep


    # SETTERS 

    @nome.setter
    def nome(self, value):
        self._nome = value

    @email.setter
    def email(self, value):
        self._email = value

    @cep.setter
    def cep(self, value):
        self._cep = value

