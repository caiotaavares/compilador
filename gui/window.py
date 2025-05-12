import tkinter as tk

def criar_janela_principal():
    root = tk.Tk()
    root.title("PCIDE - Compilador da FCT")
    root.geometry("800x600")
    root.rowconfigure(0, weight=3)
    root.rowconfigure(1, weight=4)
    root.columnconfigure(0, weight=1)
    return root
