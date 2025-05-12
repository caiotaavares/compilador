from tkinter import Menu, filedialog
from compiler.executor import executar_analise

import tkinter as tk

# ------------------------------------------------------------------------------
# 4. Criação do Menu
# ------------------------------------------------------------------------------
def criar_menu(root, text_area, tree, text_log):
    """Cria a barra de menu e adiciona ao root."""
    menubar = tk.Menu(root)

    # Menu "Arquivo"
    menu_arquivo = tk.Menu(menubar, tearoff=False)
    menu_arquivo.add_command(label="Novo")
    menu_arquivo.add_command(label="Abrir", command=lambda: abrir_arquivo(text_area))
    menu_arquivo.add_command(label="Salvar")
    menu_arquivo.add_separator()
    menu_arquivo.add_command(label="Sair", command=root.quit)
    menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

    # Menu "Editar"
    menu_editar = tk.Menu(menubar, tearoff=False)
    menu_editar.add_command(label="Desfazer")
    menu_editar.add_command(label="Refazer")
    menubar.add_cascade(label="Editar", menu=menu_editar)

    # Menu "Exibir"
    menu_exibir = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Exibir", menu=menu_exibir)

    # Menu "Localizar"
    menu_localizar = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Localizar", menu=menu_localizar)

    # Menu "Compiler"
    menu_compiler = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Compiler", menu=menu_compiler)

    # Menu "Executar" - faz a análise e preenche a tabela
    menu_executar = tk.Menu(menubar, tearoff=False)
    menu_executar.add_command(
        label="Executar",
        command=lambda: executar_analise(text_area, tree, text_log, options="executar")
    )
    menu_executar.add_command(
        label="Executar Análise Léxica",
        command=lambda: executar_analise(text_area, tree, text_log, options="analise_lexica")
    )
    menu_executar.add_command(
        label="Executar Análise Semântica",
        command=lambda: executar_analise(text_area, tree, text_log, options="analise_semantica")
    )
    menubar.add_cascade(label="Executar", menu=menu_executar)
    

    # Menu "Ajuda"
    menu_ajuda = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

    # Atribui a barra de menus à janela principal
    root.config(menu=menubar)

# ------------------------------------------------------------------------------
# 5. Abertura de Arquivo (para carregar texto no editor)
# ------------------------------------------------------------------------------
def abrir_arquivo(text_area):
    """Abre um arquivo de texto e carrega o conteúdo na área de texto."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", conteudo)
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
