# models.py

class Livro:
    def __init__(self, id_livro, titulo, autor, ano_publicacao):
        # Garante que o ID seja sempre uma string limpa (sem espaços)
        self.id_livro = str(id_livro).strip()
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao

    def to_dict(self):
        return self.__dict__

class Exemplar:
    def __init__(self, id_exemplar, id_livro, status='Disponível'):
        # Garante que os IDs sejam sempre strings limpas
        self.id_exemplar = str(id_exemplar).strip()
        self.id_livro = str(id_livro).strip()
        self.status = status
    
    def to_dict(self):
        return self.__dict__

class Usuario:
    def __init__(self, id_usuario, nome, email):
        # Garante que o ID seja sempre uma string limpa
        self.id_usuario = str(id_usuario).strip()
        self.nome = nome
        self.email = email

    def to_dict(self):
        return self.__dict__

class Emprestimo:
    def __init__(self, id_emprestimo, id_exemplar, id_usuario, data_emprestimo, data_prevista_devolucao, data_devolucao="", status_emprestimo="Ativo"):
        # Garante que os IDs sejam sempre strings limpas
        self.id_emprestimo = str(id_emprestimo).strip()
        self.id_exemplar = str(id_exemplar).strip()
        self.id_usuario = str(id_usuario).strip()
        self.data_emprestimo = data_emprestimo
        self.data_prevista_devolucao = data_prevista_devolucao
        self.data_devolucao = data_devolucao
        self.status_emprestimo = status_emprestimo
    
    def to_dict(self):
        return self.__dict__