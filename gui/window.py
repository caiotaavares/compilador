import tkinter as tk

def criar_janela_principal():
    root = tk.Tk()
    root.title("PCIDE - Calculadora/Lexer")
    root.geometry("800x600")
    root.rowconfigure(0, weight=3)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    return root
