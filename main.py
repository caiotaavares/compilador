from compiler.syntatic import tabela_sintatica
from gui.window import criar_janela_principal
from gui.editor import criar_area_principal
from gui.notebook import criar_bloco_inferior
from gui.menu import criar_menu

def main():
    root = criar_janela_principal()
    text_area = criar_area_principal(root)
    tree_lexemas, text_log, tree_sintatica = criar_bloco_inferior(root, tabela_sintatica)
    criar_menu(root, text_area, tree_lexemas, text_log, tree_sintatica)
    root.mainloop()

if __name__ == "__main__":
    main()