import tkinter as tk
from lexer.lexer import Lexer
from gui.editor import Editor
from gui.views import criar_bloco_inferior
from gui.menu import criar_menu

class LexicalAnalyzerApp:
    """Classe principal da aplicação."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PCIDE - Calculadora/Lexer")
        self.root.geometry("800x600")

        # Configurar para expandir corretamente ao redimensionar
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=3)  # Área do editor
        self.root.rowconfigure(1, weight=1)  # Área do bloco inferior (tabela e log)

        self.lexer = Lexer()
        self.editor = Editor(self.root)

        # Criar a parte inferior da interface (tabela e log)
        self.tree, self.log_text = criar_bloco_inferior(self.root)

        # Criar menu
        criar_menu(self.root, self.abrir_arquivo, self.executar_analise)

    def abrir_arquivo(self):
        """Abre um arquivo e carrega seu conteúdo na área de texto."""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            self.editor.text_area.delete("1.0", tk.END)
            self.editor.text_area.insert("1.0", conteudo)

    def executar_analise(self):
        """Executa a análise léxica e preenche a tabela de lexemas."""
        expressao = self.editor.get_text()
        tokens = self.lexer.analisar(expressao)

        # Limpa a tabela antes de adicionar novos tokens
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insere os tokens encontrados
        for lexema, token in tokens:
            tags = ("erro",) if token == "DESCONHECIDO" else ()
            self.tree.insert("", "end", values=(lexema, token), tags=tags)

        # Atualiza o log
        self.log_text.config(state='normal')
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert("1.0", "Compilação completa" if all(t[1] != "DESCONHECIDO" for t in tokens) else "Erro de compilação")
        self.log_text.config(state='disabled')

    def run(self):
        """Executa a aplicação."""
        self.root.mainloop()

if __name__ == "__main__":
    app = LexicalAnalyzerApp()
    app.run()
