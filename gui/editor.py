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
    frame_texto.columnconfigure(1, weight=1)  # Área principal expande
    
    # Widget do contador de linhas (Text com fundo cinza)
    text_line_numbers = tk.Text(
        frame_texto,
        width=2,
        bg="#f0f0f0",
        bd=0,
        highlightthickness=0,
        state='disabled'
    )
    text_line_numbers.grid(row=0, column=0, sticky="ns")
    
    # Área principal de texto
    text_area = tk.Text(frame_texto)
    text_area.grid(row=0, column=1, sticky="nsew")
    
    # Sincroniza a rolagem vertical
    def sync_scroll(*args):
        text_line_numbers.yview_moveto(args[0])
        text_area.yview_moveto(args[0])
    
    vsb = ttk.Scrollbar(frame_texto, orient="vertical", command=sync_scroll)
    text_area.config(yscrollcommand=vsb.set)
    text_line_numbers.config(yscrollcommand=vsb.set)
    vsb.grid(row=0, column=2, sticky="ns")
    
    # Função para atualizar os números de linha
    def update_line_numbers(event=None):
        text_line_numbers.config(state='normal')
        text_line_numbers.delete('1.0', tk.END)
        
        # Obtém o número de linhas
        num_lines = text_area.index(tk.END).split('.')[0]
        line_numbers = '\n'.join(str(i) for i in range(1, int(num_lines)+1))
        
        text_line_numbers.insert('1.0', line_numbers)
        text_line_numbers.config(state='disabled')
    
    # Vincula eventos que modificam o texto
    text_area.bind('<Key>', update_line_numbers)
    text_area.bind('<MouseWheel>', update_line_numbers)
    text_area.bind('<Button-4>', update_line_numbers)
    text_area.bind('<Button-5>', update_line_numbers)
    text_area.bind('<FocusIn>', update_line_numbers)
    text_area.bind('<FocusOut>', update_line_numbers)
    
    # Atualiza inicialmente
    update_line_numbers()
    
    return text_area