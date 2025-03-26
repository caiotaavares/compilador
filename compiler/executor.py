from compiler.lexer import analisar_expressao

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
def executar_analise(text_area, tree, text_log):
    """
    Lê o texto da área principal, analisa e exibe o resultado na Tabela de Lexemas.
    Também atualiza o Log de Compilação com mensagens de sucesso ou erro.
    """
    # Obtém o texto da área principal
    expressao = text_area.get("1.0", tk.END).strip()
    
    try:
        tokens = analisar_expressao(expressao)
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
    
    # Exibe a mensagem apropriada no Log de Compilação
    if has_errors:
        text_log.insert('1.0', "Erro de compilação")
        text_log.config(foreground='red')  # Define a cor do texto como vermelho
    else:
        text_log.insert('1.0', "Compilação completa")
        text_log.config(foreground='green')  # Define a cor do texto como verde
    
    # Desabilita a edição após a atualização
    text_log.config(state='disabled')