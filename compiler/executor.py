from compiler.lexer import analisar_expressao
from compiler.syntatic_analyzer import analisar_declaracoes

import tkinter as tk

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

# ------------------------------------------------------------------------------
# 3. Função de callback para o menu "Executar"
# ------------------------------------------------------------------------------
def executar_analise(text_area, tree, text_log, options):
    """
    Lê o texto da área principal, analisa e exibe o resultado na Tabela de Lexemas.
    Também atualiza o Log de Compilação com mensagens de sucesso ou erro.
    """
    # Obtém o texto da área principal
    expressao = text_area.get("1.0", tk.END).strip()
    
    try:
        if (options == "executar"):
            # Executa a análise léxica e sintática
            tokens = analisar_expressao(expressao)
            analisar_declaracoes(tokens)
            
        elif (options == "analise_lexica"):
            # Executa apenas a análise léxica
            tokens = analisar_expressao(expressao)
            msg = "Análise léxica..."
            
        elif (options == "analise_semantica"):
            # Executa apenas a análise semântica
            analisar_declaracoes(tokens)
            msg = "Análise semântica..."
            
    except SyntaxError as e:
        text_log.config(state='normal')
        text_log.delete('1.0', tk.END)
        text_log.insert('1.0', f"Erro de compilação: {e}")
        text_log.config(foreground='red', state='disabled')
        return

    
    # Limpa a tabela de lexemas antes de inserir novos resultados
    popular_tabela_lexemas(tree, tokens)
    
    # Verifica se há erros nos tokens
    has_errors = any(token['erro'] for token in tokens)
    
    # Limpa o Log de Compilação
    text_log.config(state='normal')  # Habilita a edição
    text_log.delete('1.0', tk.END)   # Limpa o conteúdo
    
    text_log.insert('1.0', get_timestamp() + msg + "\n")  # Exibe a mensagem de análise
    
    # Exibe a mensagem apropriada no Log de Compilação
    if has_errors:
        text_log.insert('2.0', get_timestamp() + "Erro de análise\n")
        text_log.config(foreground='red')  # Define a cor do texto como vermelho
    else:
        text_log.insert('2.0', get_timestamp() + "Analise concluída com sucesso!\n")
        text_log.config(foreground='green')  # Define a cor do texto como verde
    
    # Desabilita a edição após a atualização
    text_log.config(state='disabled')
    
def get_timestamp():
    """
    Retorna a data e hora atual formatada como string.
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S - ")