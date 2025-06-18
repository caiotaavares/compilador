from compiler.lexer import analisar_expressao
from compiler.syntatic_analyzer import analisar_declaracoes
from compiler.syntatic_analyzer import analisar_pascal_lark

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
    tokens = []   # <-- inicialize aqui
    # Obtém o texto da área principal
    expressao = text_area.get("1.0", tk.END).strip()
    msg = ''
    
    try:
        if (options == "executar"):
            # Executa a análise léxica e sintática
            tokens = analisar_expressao(expressao)
            analisar_declaracoes(tokens)
            
        elif (options == "analise_lexica"):
            # Executa apenas a análise léxica
            tokens = analisar_expressao(expressao)
            msg = "Análise léxica..."
            
        elif (options == "analise_semantica_lark"):
            try:
                arvore = analisar_pascal_lark(expressao)  # onde expressao é o código Pascal do editor
                print(arvore.pretty())  # ou mostre a árvore na interface
                msg = "Análise sintática concluída com sucesso!"
            except Exception as e:
                # Captura o erro do Lark e extrai a linha do erro
                erro_lark = str(e)
                # Ajuste na extração da linha para pegar apenas o número da linha
                linha_erro = erro_lark.split("line ")[-1].split(",")[0]  # Agora pegamos o número da linha corretamente
                
                # Extrai o conteúdo da linha do código
                linhas = expressao.split('\n')
                linha_conteudo = linhas[int(linha_erro) - 1] if int(linha_erro) <= len(linhas) else "Linha não encontrada"
                
                # Exibe a linha do erro no log
                msg_erro = f"Erro na linha: {linha_erro}\nConteúdo da linha: {linha_conteudo}"
                print(msg_erro)  # Para debugar na console
                
                # Exibe no log
                text_log.config(state='normal')
                text_log.delete('1.0', tk.END)
                text_log.insert('1.0', msg_erro)
                text_log.config(foreground='red', state='disabled')
                popular_tabela_lexemas(tree, tokens)   # <- Garante que sempre vai ser chamado sem erro
                return
            
    except SyntaxError as e:
        text_log.config(state='normal')
        text_log.delete('1.0', tk.END)
        text_log.insert('1.0', f"Erro de compilação: {e}")
        text_log.config(foreground='red', state='disabled')
        popular_tabela_lexemas(tree, tokens)   # <- Garante que sempre vai ser chamado sem erro
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
        text_log.insert('2.0', get_timestamp() + "Análise concluída com sucesso!\n")
        text_log.config(foreground='green')  # Define a cor do texto como verde
    
    # Desabilita a edição após a atualização
    text_log.config(state='disabled')


def get_timestamp():
    """
    Retorna a data e hora atual formatada como string.
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S - ")