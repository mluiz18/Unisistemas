class Usuario:
    def __init__(self, id_usuario, nome, email):
        self.id_usuario = str(id_usuario).strip()
        self.nome = nome
        self.email = email

    def to_dict(self):
        return self.__dict__