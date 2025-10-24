import csv
import os
import json
from models import Livro, Usuario, Emprestimo, Exemplar

DATA_DIR = 'data'
ARQUIVO_LIVROS = os.path.join(DATA_DIR, 'livros.csv')
ARQUIVO_USUARIOS = os.path.join(DATA_DIR, 'usuarios.csv')
ARQUIVO_EMPRESTIMOS = os.path.join(DATA_DIR, 'emprestimos.csv')
ARQUIVO_EXEMPLARES = os.path.join(DATA_DIR, 'exemplares.csv')
ARQUIVO_CONTADORES = os.path.join(DATA_DIR, 'contadores.json')

CABECALHO_LIVROS = ['id_livro', 'titulo', 'autor', 'ano_publicacao']
CABECALHO_USUARIOS = ['id_usuario', 'nome', 'email']
CABECALHO_EMPRESTIMOS = ['id_emprestimo', 'id_exemplar', 'id_usuario', 'data_emprestimo', 'data_prevista_devolucao', 'data_devolucao', 'status_emprestimo']
CABECALHO_EXEMPLARES = ['id_exemplar', 'id_livro', 'status']

def inicializar():
    os.makedirs(DATA_DIR, exist_ok=True)
    for arquivo, cabecalho in [(ARQUIVO_LIVROS, CABECALHO_LIVROS), 
                               (ARQUIVO_USUARIOS, CABECALHO_USUARIOS), 
                               (ARQUIVO_EMPRESTIMOS, CABECALHO_EMPRESTIMOS),
                               (ARQUIVO_EXEMPLARES, CABECALHO_EXEMPLARES)]:
        if not os.path.exists(arquivo):
            with open(arquivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(cabecalho)

    if not os.path.exists(ARQUIVO_CONTADORES):
        contadores = {
            'livro': max([int(l.id_livro) for l in _carregar(ARQUIVO_LIVROS, Livro)], default=0),
            'usuario': max([int(u.id_usuario) for u in _carregar(ARQUIVO_USUARIOS, Usuario)], default=0),
            'exemplar': max([int(e.id_exemplar) for e in _carregar(ARQUIVO_EXEMPLARES, Exemplar)], default=0),
            'emprestimo': max([int(e.id_emprestimo) for e in _carregar(ARQUIVO_EMPRESTIMOS, Emprestimo)], default=0)
        }
        _salvar_contadores(contadores)

def _carregar(arquivo, classe_modelo):
    try:
        with open(arquivo, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [classe_modelo(**row) for row in reader]
    except FileNotFoundError: return []

def _salvar(arquivo, objetos, cabecalho):
    with open(arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=cabecalho)
        writer.writeheader()
        for obj in objetos: writer.writerow(obj.to_dict())

def carregar_livros(): return _carregar(ARQUIVO_LIVROS, Livro)
def salvar_livros(livros): _salvar(ARQUIVO_LIVROS, livros, CABECALHO_LIVROS)

def carregar_usuarios(): return _carregar(ARQUIVO_USUARIOS, Usuario)
def salvar_usuarios(usuarios): _salvar(ARQUIVO_USUARIOS, usuarios, CABECALHO_USUARIOS)

def carregar_emprestimos(): return _carregar(ARQUIVO_EMPRESTIMOS, Emprestimo)
def salvar_emprestimos(emprestimos): _salvar(ARQUIVO_EMPRESTIMOS, emprestimos, CABECALHO_EMPRESTIMOS)

def carregar_exemplares(): return _carregar(ARQUIVO_EXEMPLARES, Exemplar)
def salvar_exemplares(exemplares): _salvar(ARQUIVO_EXEMPLARES, exemplares, CABECALHO_EXEMPLARES)

def _ler_contadores():
    try:
        with open(ARQUIVO_CONTADORES, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        inicializar()
        with open(ARQUIVO_CONTADORES, 'r', encoding='utf-8') as f:
            return json.load(f)

def _salvar_contadores(contadores):
    with open(ARQUIVO_CONTADORES, 'w', encoding='utf-8') as f:
        json.dump(contadores, f, indent=4)

def obter_proximo_id(tipo):
    contadores = _ler_contadores()

    ultimo_id = contadores.get(tipo, 0)

    novo_id = ultimo_id + 1

    contadores[tipo] = novo_id

    _salvar_contadores(contadores)
    
    return novo_id