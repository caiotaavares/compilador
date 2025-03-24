import tkinter as tk
from tkinter import ttk

class Editor:
    """Classe responsável pela área de texto com numeração de linhas e scroll."""

    def __init__(self, root):
        self.frame_texto = ttk.Frame(root)
        self.frame_texto.grid(row=0, column=0, sticky="nsew")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=3)

        # Criando Scrollbars
        self.scroll_y = ttk.Scrollbar(self.frame_texto, orient="vertical")
        self.scroll_x = ttk.Scrollbar(self.frame_texto, orient="horizontal")

        # Criando a área de numeração de linhas
        self.text_line_numbers = tk.Text(
            self.frame_texto,
            width=4, bg="#f0f0f0", bd=0,
            state='disabled',
            yscrollcommand=self.scroll_y.set
        )
        self.text_line_numbers.grid(row=0, column=0, sticky="ns")

        # Criando a área de texto principal
        self.text_area = tk.Text(
            self.frame_texto,
            wrap="none",  # Sem quebra automática de linha
            yscrollcommand=self._sync_scroll_y,
            xscrollcommand=self.scroll_x.set
        )
        self.text_area.grid(row=0, column=1, sticky="nsew")

        # Configurar scrollbars
        self.scroll_y.config(command=self._sync_scroll_y_both)
        self.scroll_y.grid(row=0, column=2, sticky="ns")

        self.scroll_x.config(command=self.text_area.xview)
        self.scroll_x.grid(row=1, column=1, sticky="ew")

        # Configurar expansão
        self.frame_texto.columnconfigure(1, weight=1)
        self.frame_texto.rowconfigure(0, weight=1)

        # Vincular eventos para atualizar a numeração de linhas
        self.text_area.bind("<KeyRelease>", self.atualizar_numero_linhas)
        self.text_area.bind("<MouseWheel>", self.atualizar_numero_linhas)
        self.text_area.bind("<Button-4>", self.atualizar_numero_linhas)  # Scroll para cima (Linux)
        self.text_area.bind("<Button-5>", self.atualizar_numero_linhas)  # Scroll para baixo (Linux)
        self.text_area.bind("<FocusIn>", self.atualizar_numero_linhas)

        # Atualizar números de linha inicialmente
        self.atualizar_numero_linhas()

    def get_text(self):
        return self.text_area.get("1.0", tk.END).strip()

    def atualizar_numero_linhas(self, event=None):
        """Atualiza a numeração de linhas e sincroniza com a rolagem."""
        self.text_line_numbers.config(state='normal')
        self.text_line_numbers.delete('1.0', tk.END)

        num_linhas = int(self.text_area.index(tk.END).split('.')[0])
        linha_atual = int(self.text_area.index(tk.INSERT).split('.')[0])

        numeros = "\n".join(str(i) for i in range(1, num_linhas))
        self.text_line_numbers.insert("1.0", numeros)
        self.text_line_numbers.config(state='disabled')

        # Ajusta rolagem automaticamente para manter a linha atual visível
        self.text_line_numbers.yview_moveto(self.text_area.yview()[0])

    def _sync_scroll_y(self, *args):
        """Sincroniza a rolagem vertical da área de texto."""
        self.text_area.yview(*args)
        self.text_line_numbers.yview(*args)

    def _sync_scroll_y_both(self, *args):
        """Sincroniza a rolagem da barra de rolagem e a numeração de linhas."""
        self._sync_scroll_y(*args)
        self.text_line_numbers.yview_moveto(args[0])
