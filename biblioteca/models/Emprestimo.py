class Emprestimo:
    def __init__(self, id_emprestimo, id_exemplar, id_usuario, data_emprestimo, data_prevista_devolucao, data_devolucao="", status_emprestimo="Ativo"):
        self.id_emprestimo = str(id_emprestimo).strip()
        self.id_exemplar = str(id_exemplar).strip()
        self.id_usuario = str(id_usuario).strip()
        self.data_emprestimo = data_emprestimo
        self.data_prevista_devolucao = data_prevista_devolucao
        self.data_devolucao = data_devolucao
        self.status_emprestimo = status_emprestimo
    
    def to_dict(self):
        return self.__dict__