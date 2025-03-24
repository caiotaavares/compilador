import tkinter as tk

def criar_menu(root, abrir_arquivo, executar_analise):
    """Cria a barra de menus."""
    menubar = tk.Menu(root)

    menu_arquivo = tk.Menu(menubar, tearoff=False)
    menu_arquivo.add_command(label="Abrir", command=abrir_arquivo)
    menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

    menu_executar = tk.Menu(menubar, tearoff=False)
    menu_executar.add_command(label="Executar Análise", command=executar_analise)
    menubar.add_cascade(label="Executar", menu=menu_executar)

    root.config(menu=menubar)
