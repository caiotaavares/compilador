from compiler.lexer import analisar_expressao
from compiler.syntatic_analyzer import analisar_declaracoes
from compiler.semantic_analyzer import build_symbol_table, check_semantics
from compiler.bytecode import generate_bytecode
import tkinter as tk
from datetime import datetime

# ------------------------------------------------------------------------------
# 2. Função para popular o Treeview com o resultado da análise
# ------------------------------------------------------------------------------
def popular_tabela_lexemas(tree, tokens):
    """
    Recebe o Treeview (tabela) e a lista de tokens gerada por analisar_expressao().
    Limpa a tabela e insere os novos valores.
    """
    # Remove itens antigos
    for item in tree.get_children():
        tree.delete(item)

    # Insere os novos tokens
        
    for t in tokens:
        # Define a tag se for um token desconhecido
        tags = ('erro',) if t['token'] == "DESCONHECIDO" else ()
        
        tree.insert(
            "", "end", 
            values=(
                t['lexema'], t['token'], t['erro'],
                t['linha'], t['col_ini'], t['col_fim']
            ),
            tags=tags  # Aplica a tag aqui
        )

# Esta função é chamada ao clicar em "Executar" no editor
def executar_analise(text_area, tree, text_log, options):
    """
    Lê o texto da área principal, analisa e exibe o resultado na Tabela de Lexemas.
    Também atualiza o Log de Compilação com mensagens de sucesso ou erro.
    Inclui checagem semântica de identificadores e procedures.
    """
    # 1) Análise léxica
    expressao = text_area.get("1.0", tk.END).strip()
    try:
        tokens = analisar_expressao(expressao)

        # 2) Análise sintática LL(1)
        if options == "executar":
            analisar_declaracoes(tokens)

            # 3) Construção da tabela de símbolos e checagem semântica
            symtab = build_symbol_table(tokens)
            semantic_errors = check_semantics(tokens, symtab)
            if semantic_errors:
                raise SyntaxError("\n".join(semantic_errors))
            bytecode = generate_bytecode(tokens)
            # exiba no text_log ou em outro painel
            text_log.config(state='normal')
            text_log.delete('1.0', tk.END)
            text_log.insert('1.0', "Bytecode gerado:\n" + "\n".join(bytecode))
            text_log.config(foreground='black', state='disabled')
            salvar_resultado(bytecode)
            return

        elif options == "analise_lexica":
            # somente léxico: nada adicional a fazer
            pass
        else:
            # outras opções não usadas
            pass

    except SyntaxError as e:
        # Exibe erros sintáticos ou semânticos
        text_log.config(state='normal')
        text_log.delete('1.0', tk.END)
        text_log.insert('1.0', f"Erro de compilação: {e}")
        text_log.config(foreground='red', state='disabled')
        # Atualiza tabela de lexemas mesmo em erro
        popular_tabela_lexemas(tree, tokens)
        return

    # Se chegou aqui, não houve erros
    # Atualiza tabela de lexemas
    popular_tabela_lexemas(tree, tokens)

    # Mensagem de sucesso
    text_log.config(state='normal')
    text_log.delete('1.0', tk.END)
    text_log.insert('1.0', get_timestamp() + "Análise concluída com sucesso!\n")
    text_log.config(foreground='green', state='disabled')


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S - ")

def salvar_resultado(bytecode):
    """Salva o bytecode no arquivo 'resultado' na raiz do projeto."""
    with open('resultado', 'w', encoding='utf-8') as f:
        for ins in bytecode:
            f.write(ins + '\n')