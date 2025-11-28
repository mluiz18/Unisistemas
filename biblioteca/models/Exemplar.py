class Exemplar:
    def __init__(self, id_exemplar, id_livro, status='Disponível'):
        # Garante que os IDs sejam sempre strings limpas
        self.id_exemplar = str(id_exemplar).strip()
        self.id_livro = str(id_livro).strip()
        self.status = status
    
    def to_dict(self):
        return self.__dict__
