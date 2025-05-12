import tkinter as tk
from tkinter import ttk

# ------------------------------------------------------------------------------
# 7. Criação do bloco inferior com Notebook (duas abas)
# ------------------------------------------------------------------------------
def criar_bloco_inferior(root, tabela_sintatica):
    """Cria o bloco inferior com três abas: Log, Tabela de Lexemas e Tabela Sintática."""
    notebook = ttk.Notebook(root)
    notebook.grid(row=1, column=0, sticky="nsew")

    # Aba: Log de Compilação
    frame_log = ttk.Frame(notebook)
    text_log = tk.Text(frame_log)
    text_log.pack(expand=True, fill="both")
    notebook.add(frame_log, text="Log de Compilação")

    # Aba: Tabela de Lexemas
    frame_lexemas = ttk.Frame(notebook)
    colunas_lexemas = ("Lexema", "Token", "Erro", "Linha", "ColIni", "ColFim")
    tree_lexemas = ttk.Treeview(frame_lexemas, columns=colunas_lexemas, show="headings", height=8)

    for col in colunas_lexemas:
        tree_lexemas.heading(col, text=col)
        tree_lexemas.column(col, width=100)

    tree_lexemas.pack(expand=True, fill="both")
    notebook.add(frame_lexemas, text="Tabela de Lexemas")

    # Aba: Tabela Sintática
    frame_tabela = ttk.Frame(notebook)
    
    terminais = obter_todos_terminais(tabela_sintatica)
    colunas_sintatica = ["Não Terminal"] + terminais
    tree_sintatica = ttk.Treeview(frame_tabela, columns=colunas_sintatica, show="headings", height=10)

    for col in colunas_sintatica:
        tree_sintatica.heading(col, text=col)
        tree_sintatica.column(col, width=200)

    # Preencher a tabela
    for nao_terminal in tabela_sintatica:
        linha = [nao_terminal]
        for terminal in terminais:
            producao = tabela_sintatica[nao_terminal].get(terminal, '-')
            if isinstance(producao, list):
                producao = f"{nao_terminal} → " + ' '.join(producao)
            linha.append(producao)
        tree_sintatica.insert("", "end", values=linha)

    tree_sintatica.pack(expand=True, fill="both")
    notebook.add(frame_tabela, text="Tabela Sintática")

    return tree_lexemas, text_log

def obter_todos_terminais(tabela):
    terminais = set()
    for producoes in tabela.values():
        terminais.update(producoes.keys())
    return sorted(terminais)
