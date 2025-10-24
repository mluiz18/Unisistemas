import gerenciador_dados as db
from models import Livro, Usuario, Emprestimo, Exemplar
from datetime import datetime, timedelta

class Biblioteca:
    def __init__(self):
        db.inicializar()
        self._carregar_dados()

    def _carregar_dados(self):
        self.livros = db.carregar_livros()
        self.usuarios = db.carregar_usuarios()
        self.exemplares = db.carregar_exemplares()
        self.emprestimos = db.carregar_emprestimos()

    def adicionar_livro(self, titulo, autor, ano_publicacao, qtd_inicial=1):
        novo_id_livro = db.obter_proximo_id('livro')
        novo_livro = Livro(novo_id_livro, titulo, autor, ano_publicacao)
        self.livros.append(novo_livro)
        
        proximo_id_exemplar = db.obter_proximo_id('exemplar')
        for i in range(qtd_inicial):
            self.exemplares.append(Exemplar(proximo_id_exemplar + i, novo_id_livro))
            
        db.salvar_livros(self.livros)
        db.salvar_exemplares(self.exemplares)
        return novo_livro

    def adicionar_usuario(self, nome, email):
        novo_id = db.obter_proximo_id('usuario')
        novo_usuario = Usuario(novo_id, nome, email)
        self.usuarios.append(novo_usuario)
        db.salvar_usuarios(self.usuarios)
        return novo_usuario

    def realizar_emprestimo(self, id_livro, id_usuario, data_devolucao):
        if not any(u.id_usuario == str(id_usuario) for u in self.usuarios):
            raise ValueError(f"Usuário com ID {id_usuario} não encontrado.")
        
        exemplar_disponivel = next((ex for ex in self.exemplares if ex.id_livro == str(id_livro) and ex.status == 'Disponível'), None)
        if not exemplar_disponivel:
            raise ValueError(f"Nenhum exemplar do livro com ID {id_livro} está disponível.")
            
        exemplar_disponivel.status = 'Emprestado'
        novo_id = db.obter_proximo_id('emprestimo')
        data_emp = datetime.now().strftime('%Y-%m-%d')
        novo_emprestimo = Emprestimo(novo_id, exemplar_disponivel.id_exemplar, id_usuario, data_emp, data_devolucao)
        self.emprestimos.append(novo_emprestimo)
        
        db.salvar_exemplares(self.exemplares)
        db.salvar_emprestimos(self.emprestimos)
        return novo_emprestimo

    def devolver_livro(self, id_emprestimo):
        emprestimo = next((emp for emp in self.emprestimos if emp.id_emprestimo == str(id_emprestimo)), None)
        if not emprestimo:
            raise ValueError(f"Empréstimo com ID {id_emprestimo} não encontrado.")
        
        exemplar = next((ex for ex in self.exemplares if ex.id_exemplar == emprestimo.id_exemplar), None)
        if exemplar:
            exemplar.status = 'Disponível'
        
        self.emprestimos.remove(emprestimo)
        
        db.salvar_exemplares(self.exemplares)
        db.salvar_emprestimos(self.emprestimos)
        return True

    def buscar_livros(self, termo):
        termo = termo.lower()
        return [livro for livro in self.livros if termo in livro.titulo.lower() or termo in livro.autor.lower()]

    def buscar_usuarios(self, termo):
        termo = termo.lower()
        return [user for user in self.usuarios if termo in user.nome.lower() or termo in user.email.lower()]

    def listar_emprestimos_ativos(self, formatado=True):
        if not formatado:
            return self.emprestimos
        
        dados_formatados = []
        mapa_usuarios = {user.id_usuario: user.nome for user in self.usuarios}
        mapa_exemplares = {ex.id_exemplar: ex.id_livro for ex in self.exemplares}
        mapa_livros = {livro.id_livro: livro.titulo for livro in self.livros}
        for emprestimo in self.emprestimos:
            nome_usuario = mapa_usuarios.get(emprestimo.id_usuario, "N/A")
            id_livro = mapa_exemplares.get(emprestimo.id_exemplar)
            titulo_livro = mapa_livros.get(id_livro, "N/A")
            info_exemplar = f"{titulo_livro} (Ex. {emprestimo.id_exemplar})"
            dados_formatados.append({
                "id_emprestimo": emprestimo.id_emprestimo, "info_exemplar": info_exemplar,
                "nome_usuario": nome_usuario, "data_emprestimo": emprestimo.data_emprestimo,
                "data_prevista_devolucao": emprestimo.data_prevista_devolucao
            })
        return dados_formatados
        
if __name__ == "__main__":
    
    biblioteca = Biblioteca()
    print(">>> Instância da biblioteca criada.\n")

    print(">>> Adicionando um novo usuário...")
    try:
        novo_usuario = biblioteca.adicionar_usuario("Ana Silva", "ana.silva@email.com")
        print(f"Usuário '{novo_usuario.nome}' (ID: {novo_usuario.id_usuario}) adicionado com sucesso!\n")
    except Exception as e:
        print(f"Erro: {e}\n")

    print(">>> Adicionando um novo livro com 2 exemplares...")
    try:
        novo_livro = biblioteca.adicionar_livro("O Senhor dos Anéis", "J.R.R. Tolkien", "1954", qtd_inicial=2)
        print(f"Livro '{novo_livro.titulo}' (ID: {novo_livro.id_livro}) e seus exemplares adicionados!\n")
    except Exception as e:
        print(f"Erro: {e}\n")

    print(">>> Realizando um empréstimo...")
    try:
        id_livro_para_emprestar = novo_livro.id_livro
        id_usuario_que_empresta = novo_usuario.id_usuario
        data_fim = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        
        emprestimo_realizado = biblioteca.realizar_emprestimo(id_livro_para_emprestar, id_usuario_que_empresta, data_fim)
        print(f"Empréstimo (ID: {emprestimo_realizado.id_emprestimo}) realizado com sucesso!\n")
    except ValueError as e:
        print(f"Erro ao realizar empréstimo: {e}\n")

    print(">>> Listando empréstimos ativos:")
    emprestimos_ativos = biblioteca.listar_emprestimos_ativos()
    if not emprestimos_ativos:
        print("Nenhum empréstimo ativo no momento.")
    else:
        for emp in emprestimos_ativos:
            print(f"- ID: {emp['id_emprestimo']}, Livro: {emp['info_exemplar']}, Usuário: {emp['nome_usuario']}, Devolução: {emp['data_prevista_devolucao']}")
    print("\n")

    print(">>> Tentando emprestar o mesmo livro novamente (deve falhar)...")
    try:
        biblioteca.realizar_emprestimo(novo_livro.id_livro, novo_usuario.id_usuario, data_fim)
    except ValueError as e:
        print(f"Sucesso! O erro esperado aconteceu: {e}\n")

    id_emprestimo_para_devolver = emprestimo_realizado.id_emprestimo
    print(f">>> Devolvendo o livro do empréstimo ID {id_emprestimo_para_devolver}...")
    try:
        biblioteca.devolver_livro(id_emprestimo_para_devolver)
        print("Devolução realizada com sucesso!\n")
    except ValueError as e:
        print(f"Erro ao devolver: {e}\n")
        
    print(">>> Listando empréstimos ativos novamente:")
    emprestimos_ativos = biblioteca.listar_emprestimos_ativos()
    if not emprestimos_ativos:
        print("Nenhum empréstimo ativo no momento.\n")