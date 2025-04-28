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
# 1. Função de análise sintática para declarações de variáveis
# FORMA GERAL
# decl_var -> 'var' lista_decl_var
# lista_decl_var -> lista_id ':' tipo ';' lista_decl_var | ε
# lista_id -> id lista_id_tail
# lista_id_tail -> ',' id lista_id_tail | ε
# tipo -> 'int' | 'boolean'
# id -> IDENTIFICADOR
# ------------------------------------------------------------------------------
def analisar_declaracoes(tokens):
    """
    Analisa uma sequência de tokens para declaração de variáveis.
    Levanta exceções se encontrar erros sintáticos.
    """

    pos = 0
    tamanho = len(tokens)

    def token_atual():
        return tokens[pos] if pos < tamanho else None

    def consumir(tipo_esperado):
        nonlocal pos
        tok = token_atual()
        if tok and tok['token'] == tipo_esperado:
            pos += 1
        else:
            esperado = tipo_esperado.replace('PALAVRA_RESERVADA_', '').lower()
            encontrado = tok['lexema'] if tok else 'EOF'
            raise SyntaxError(f"Erro de sintaxe: esperado '{esperado}', encontrado '{encontrado}' na linha {tok['linha'] if tok else 'final do arquivo'}.")

    def decl_var():
        consumir('PALAVRA_RESERVADA_VAR')
        lista_decl_var()

    def lista_decl_var():
        tok = token_atual()
        if tok and tok['token'] == 'IDENTIFICADOR':
            lista_id()
            consumir('SEPARADOR')  # Espera ':'
            tipo()
            consumir('PONTO_E_VIRGULA')
            lista_decl_var()
        # Se não for identificador, pode ser ε (vazio)

    def lista_id():
        consumir('IDENTIFICADOR')
        lista_id_tail()

    def lista_id_tail():
        tok = token_atual()
        if tok and tok['token'] == 'VIRGULA':
            consumir('VIRGULA')
            consumir('IDENTIFICADOR')
            lista_id_tail()
        # ε (nada a fazer)

    def tipo():
        tok = token_atual()
        if tok and (tok['token'] == 'PALAVRA_RESERVADA_INT' or tok['token'] == 'PALAVRA_RESERVADA_BOOLEAN'):
            consumir(tok['token'])
        else:
            esperado = "'int' ou 'boolean'"
            encontrado = tok['lexema'] if tok else 'EOF'
            raise SyntaxError(f"Erro de sintaxe: esperado {esperado}, encontrado '{encontrado}' na linha {tok['linha'] if tok else 'final do arquivo'}.")

    # Início da análise
    decl_var()

    if pos < tamanho:
        resto = token_atual()
        raise SyntaxError(f"Erro: tokens inesperados após declaração de variáveis, começando em '{resto['lexema']}' linha {resto['linha']}.")

    return True  # Análise sintática foi bem-sucedida

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
        analisar_declaracoes(tokens)
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