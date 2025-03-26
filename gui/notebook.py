import tkinter as tk
from tkinter import ttk

# ------------------------------------------------------------------------------
# 7. Criação do bloco inferior com Notebook (duas abas)
# ------------------------------------------------------------------------------
def criar_bloco_inferior(root):
    """Cria o bloco inferior com abas. Retorna o Treeview da aba 'Tabela de Lexemas' e o Text do Log."""
    notebook = ttk.Notebook(root)
    notebook.grid(row=1, column=0, sticky="nsew")

    # Frame para "Log de Compilação"
    frame_log = ttk.Frame(notebook)
    text_log = tk.Text(frame_log)
    text_log.pack(expand=True, fill="both")
    notebook.add(frame_log, text="Log de Compilação")

    # Frame para "Tabela de Lexemas"
    frame_lexemas = ttk.Frame(notebook)
    colunas = ("Lexema", "Token", "Erro", "Linha", "ColIni", "ColFim")
    tree_lexemas = ttk.Treeview(frame_lexemas, columns=colunas, show="headings", height=8)
    
    # Configura o heading (título das colunas)
    for col in colunas:
        tree_lexemas.heading(col, text=col)
        tree_lexemas.column(col, width=100)
    
    tree_lexemas.pack(expand=True, fill="both")
    notebook.add(frame_lexemas, text="Tabela de Lexemas")
    
    return tree_lexemas, text_log