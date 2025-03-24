import tkinter as tk
from tkinter import ttk

def criar_bloco_inferior(root):
    """Cria o bloco inferior com abas e adiciona Scrolls."""

    notebook = ttk.Notebook(root)
    notebook.grid(row=1, column=0, sticky="nsew")

    root.rowconfigure(1, weight=1)

    # -----------------------
    # 📌 Log de Compilação
    # -----------------------
    frame_log = ttk.Frame(notebook)

    scroll_y_log = ttk.Scrollbar(frame_log, orient="vertical")
    scroll_x_log = ttk.Scrollbar(frame_log, orient="horizontal")

    log_text = tk.Text(
        frame_log,
        wrap="none",
        yscrollcommand=scroll_y_log.set,
        xscrollcommand=scroll_x_log.set
    )
    log_text.pack(expand=True, fill="both")

    # Configurar os scrolls
    scroll_y_log.config(command=log_text.yview)
    scroll_y_log.pack(side="right", fill="y")

    scroll_x_log.config(command=log_text.xview)
    scroll_x_log.pack(side="bottom", fill="x")

    notebook.add(frame_log, text="Log de Compilação")

    # -----------------------
    # Tabela de Lexemas
    # -----------------------
    frame_lexemas = ttk.Frame(notebook)

    colunas = ("Lexema", "Token")
    tree = ttk.Treeview(
        frame_lexemas,
        columns=colunas,
        show="headings",
        height=8
    )

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    # Criar Scrollbars
    scroll_y_table = ttk.Scrollbar(frame_lexemas, orient="vertical", command=tree.yview)
    scroll_x_table = ttk.Scrollbar(frame_lexemas, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=scroll_y_table.set, xscrollcommand=scroll_x_table.set)

    # Posicionar elementos
    tree.pack(expand=True, fill="both")
    scroll_y_table.pack(side="right", fill="y")
    scroll_x_table.pack(side="bottom", fill="x")

    notebook.add(frame_lexemas, text="Tabela de Lexemas")

    # Estilo para token desconhecido
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.map("Treeview")

    # Tag personalizada para erros
    tree.tag_configure("erro", background="red", foreground="white")

    return tree, log_text
