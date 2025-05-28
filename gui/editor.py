from tkinter import ttk
import tkinter as tk

# ------------------------------------------------------------------------------
# 6. Criação da área principal de texto
# ------------------------------------------------------------------------------
def criar_area_principal(root):
    """Cria a área principal (como um editor de texto) e a posiciona na janela."""
     # Frame para conter o contador e o texto
    frame_texto = ttk.Frame(root)
    frame_texto.grid(row=0, column=0, sticky="nsew")
    frame_texto.columnconfigure(1, weight=1)
    
    # Widget do contador de linhas (Text com fundo cinza)
    text_line_numbers = tk.Text(
        frame_texto,
        width=4,
        bg="#f0f0f0",
        bd=0,
        highlightthickness=0,
        state='disabled',
        takefocus=0
    )
    text_line_numbers.grid(row=0, column=0, sticky="ns")
    
    # Área principal de texto
    text_area = tk.Text(frame_texto)
    text_area.grid(row=0, column=1, sticky="nsew")
    
    # Função para atualizar os números de linha
    def update_line_numbers(event=None):
        text_line_numbers.config(state='normal')
        text_line_numbers.delete('1.0', tk.END)
        
        # Obtém a primeira linha visível
        first_visible = text_area.index("@0,0")
        last_visible = text_area.index("@0,%d" % text_area.winfo_height())
        
        first_line = int(float(first_visible))
        last_line = int(float(last_visible)) + 1
        
        # Gera números apenas para as linhas visíveis
        line_numbers = '\n'.join(str(i).rjust(3) for i in range(first_line, last_line))
        
        text_line_numbers.insert('1.0', line_numbers)
        text_line_numbers.config(state='disabled')
        
        # Sincroniza a posição de rolagem
        text_line_numbers.yview_moveto(text_area.yview()[0])
    
    # Sincroniza a rolagem vertical
    def on_scroll(*args):
        if len(args) > 1:
            # Movimento do scrollbar
            text_area.yview_moveto(args[0])
            text_line_numbers.yview_moveto(args[0])
        else:
            # Movimento do mouse wheel
            text_area.yview_scroll(args[0], "units")
            text_line_numbers.yview_scroll(args[0], "units")
        update_line_numbers()
    
    vsb = ttk.Scrollbar(frame_texto, orient="vertical", command=on_scroll)
    text_area.config(yscrollcommand=vsb.set)
    text_line_numbers.config(yscrollcommand=vsb.set)
    vsb.grid(row=0, column=2, sticky="ns")
    
    # Vincula eventos que modificam o texto ou a visualização
    text_area.bind('<<Modified>>', update_line_numbers)
    text_area.bind('<Configure>', update_line_numbers)
    text_area.bind('<MouseWheel>', lambda e: on_scroll(-1 if e.delta > 0 else 1))
    text_area.bind('<Button-4>', lambda e: on_scroll(-1))  # Linux scroll up
    text_area.bind('<Button-5>', lambda e: on_scroll(1))   # Linux scroll down
    
    # Atualiza inicialmente
    update_line_numbers()
    
    return text_area