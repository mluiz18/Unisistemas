class Livro:
    def __init__(self, id_livro, titulo, autor, ano_publicacao):
        self.id_livro = str(id_livro).strip()
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao

    def to_dict(self):
        return self.__dict__