from compiler.lexer import analisar_expressao
from compiler.syntatic_analyzer import tabela_sintatica
from datetime import datetime
import tkinter as tk
from lark import Lark

# Função de timestamp
def get_timestamp():
    """Retorna um timestamp formatado para o log."""
    return datetime.now().strftime("[%H:%M:%S] ")

# Função de análise sintática com Lark
def analisar_pascal_lark(codigo_fonte, caminho_gramatica="grammar.lark"):
    # Lê a gramática do arquivo
    with open(caminho_gramatica, "r", encoding="utf-8") as f:
        gramatica = f.read()

    # Cria o parser do Lark
    parser = Lark(gramatica, start="start", parser="lalr")
    
    # Faz o parse do código-fonte
    arvore = parser.parse(codigo_fonte)
    
    return arvore

# Função para popular a tabela de lexemas
def popular_tabela_lexemas(tree, tokens):
    for item in tree.get_children():
        tree.delete(item)
    
    for t in tokens:
        tags = ('erro',) if t['token'] == "DESCONHECIDO" else ()
        tree.insert("", "end", 
                    values=(t['lexema'], t['token'], t['erro'], t['linha'], t['col_ini'], t['col_fim']),
                    tags=tags)

# Função para popular a tabela sintática
def popular_tabela_sintatica(tree_sintatica):
    try:
        # Tenta importar localmente se não for global
        from compiler.syntatic_analyzer import tabela_sintatica
    except ImportError:
        print("ERRO CRÍTICO: Não foi possível encontrar 'tabela_sintatica'. Verifique a importação em executor.py")
        return
    
    try:
        for item in tree_sintatica.get_children():
            tree_sintatica.delete(item)

        colunas_interface = tree_sintatica["columns"]
        
        for nao_terminal in sorted(tabela_sintatica.keys()):
            linha_valores = [nao_terminal]
            for terminal_coluna in colunas_interface[1:]:
                producao_valor = tabela_sintatica.get(nao_terminal, {}).get(terminal_coluna, '-')
                if isinstance(producao_valor, list):
                    producao_formatada = f"{nao_terminal} ⟶ {' '.join(str(x) for x in producao_valor)}"
                elif producao_valor == 'ε':
                    producao_formatada = f"{nao_terminal} ⟶ ε"
                else:
                    producao_formatada = '-'
                linha_valores.append(producao_formatada)

            tree_sintatica.insert("", "end", values=tuple(linha_valores))

    except Exception as e:
        print(f"Erro GERAL e INESPERADO dentro de popular_tabela_sintatica: {str(e)}")
        import traceback
        traceback.print_exc()

# Função de callback para o menu "Executar"
def executar_analise(text_area, tree, text_log, options, tree_sintatica):
    """
    Lê o texto da área principal, analisa e exibe o resultado na Tabela de Lexemas.
    Também atualiza o Log de Compilação com mensagens de sucesso ou erro.
    """
    print(f"\nExecutando análise com opção: {options}")
    
    # Obtém o texto da área principal
    expressao = text_area.get("1.0", tk.END).strip()
    print(f"Texto para análise: {expressao[:50]}...")  # Mostra os primeiros 50 caracteres
    
    msg = ''
    tokens = None
    
    try:
        # Sempre executa a análise léxica primeiro para obter os tokens
        tokens = analisar_expressao(expressao)
        print(f"Análise léxica gerou {len(tokens)} tokens")
        
        if options == "executar":
            print("Iniciando análise sintática com Lark...")
            arvore = analisar_pascal_lark(expressao)  # Usando Lark para análise sintática
            msg = "Análise sintática com Lark concluída com sucesso!"
            # Preenche a tabela sintática com o resultado
            print("Chamando popular_tabela_sintatica...")
            popular_tabela_sintatica(tree_sintatica)
            
        elif options == "analise_lexica":
            msg = "Análise léxica concluída com sucesso!"
            
        elif options == "analise_semantica":
            # Adapte conforme a lógica semântica do seu compilador
            msg = "Análise semântica concluída com sucesso!"
            
    except SyntaxError as e:
        text_log.config(state='normal')
        text_log.delete('1.0', tk.END)
        text_log.insert('1.0', f"Erro de sintaxe: {str(e)}\n")
        text_log.config(foreground='red', state='disabled')
        return
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        text_log.config(state='normal')
        text_log.delete('1.0', tk.END)
        text_log.insert('1.0', f"Erro inesperado: {str(e)}\n")
        text_log.config(foreground='red', state='disabled')
        return
    
    if tokens:  # Só popula a tabela de lexemas se tivermos tokens
        # Limpa a tabela de lexemas antes de inserir novos resultados
        popular_tabela_lexemas(tree, tokens)
        
        # Verifica se há erros nos tokens
        has_errors = any(token['erro'] for token in tokens)
        
        # Limpa o Log de Compilação
        text_log.config(state='normal')  # Habilita a edição
        text_log.delete('1.0', tk.END)   # Limpa o conteúdo
        
        text_log.insert('1.0', get_timestamp() + msg + "\n")  # Exibe a mensagem de análise
        
        if has_errors:
            text_log.insert('2.0', get_timestamp() + "Erro de análise\n")
            text_log.config(foreground='red')  # Define a cor do texto como vermelho
        else:
            text_log.insert('2.0', get_timestamp() + "Análise concluída com sucesso!\n")
            text_log.config(foreground='green')  # Define a cor do texto como verde
        
        text_log.config(state='disabled')  # Desabilita a edição
