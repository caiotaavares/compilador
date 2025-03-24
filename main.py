import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import re

def criar_janela_principal():
    """Cria a janela principal e retorna o objeto root."""
    root = tk.Tk()
    root.title("PCIDE - Calculadora/Lexer")
    root.geometry("800x600")

    # Configura o grid para redimensionamento
    root.rowconfigure(0, weight=3)  # Área de texto principal
    root.rowconfigure(1, weight=1)  # Aba inferior (tabela)
    root.columnconfigure(0, weight=1)
    
    root.rowconfigure(0, weight=3)  # Área principal expande verticalmente
    root.columnconfigure(0, weight=1)  # Área principal expande horizontalmente

    return root

# ------------------------------------------------------------------------------
# 1. Função de análise léxica
# ------------------------------------------------------------------------------
import re

def analisar_expressao(expressao):
    """Faz uma análise léxica completa da expressão usando regex."""
    tokens_encontrados = []
    linha = 1  # Para simplificar, consideramos que tudo começa na linha 1

    # Tabela de palavras reservadas
    palavras_reservadas = {
        "program": "PALAVRA_RESERVADA_PROGRAM",
        "begin": "PALAVRA_RESERVADA_BEGIN",
        "end": "PALAVRA_RESERVADA_END",
        "if": "PALAVRA_RESERVADA_IF",
        "then": "PALAVRA_RESERVADA_THEN",
        "else": "PALAVRA_RESERVADA_ELSE",
        "while": "PALAVRA_RESERVADA_WHILE",
        "do": "PALAVRA_RESERVADA_DO",
        "procedure": "PALAVRA_RESERVADA_PROCEDURE",
        "var": "PALAVRA_RESERVADA_VAR",
        "int": "PALAVRA_RESERVADA_INT",
        "boolean": "PALAVRA_RESERVADA_BOOLEAN",
        "true": "PALAVRA_RESERVADA_TRUE",
        "false": "PALAVRA_RESERVADA_FALSE",
        "read": "PALAVRA_RESERVADA_READ",
        "write": "PALAVRA_RESERVADA_WRITE"
    }

    # Definição das expressões regulares
    regex_tokens = [
        (r'\b(program|begin|end|if|then|else|while|do|procedure|var|int|boolean|true|false|read|write)\b', lambda match: ('PALAVRA_RESERVADA_' + match.group(0).upper(), match.group(0))),
        (r'[a-zA-Z_][a-zA-Z0-9_]*', lambda match: ('IDENTIFICADOR', match.group(0))),
        (r'\d+(\.\d+)?', lambda match: ('NUMERO_REAL' if '.' in match.group(0) else 'NUMERO_INTEIRO', match.group(0))),
        (r'::=', lambda match: ('ATRIBUICAO', '::=')),
        (r':', lambda match: ('SEPARADOR', ':')),
        (r'==', lambda match: ('IGUALDADE', '==')),
        (r'<>', lambda match: ('DIFERENTE', '<>')),
        (r'<=', lambda match: ('MENOR_IGUAL', '<=')),
        (r'>=', lambda match: ('MAIOR_IGUAL', '>=')),
        (r'<', lambda match: ('MENOR', '<')),
        (r'>', lambda match: ('MAIOR', '>')),
        (r'\(', lambda match: ('ABRE_PARENTESES', '(')),
        (r'\)', lambda match: ('FECHA_PARENTESES', ')')),
        (r'\{', lambda match: ('ABRE_CHAVES', '{')),
        (r'\}', lambda match: ('FECHA_CHAVES', '}')),
        (r'\[', lambda match: ('ABRE_COLCHETES', '[')),
        (r'\]', lambda match: ('FECHA_COLCHETES', ']')),
        (r'\+', lambda match: ('OPERADOR_SOMA', '+')),
        (r'-', lambda match: ('OPERADOR_SUBTRACAO', '-')),
        (r'\*', lambda match: ('OPERADOR_MULTIPLICACAO', '*')),
        (r'/', lambda match: ('OPERADOR_DIVISAO', '/')),
        (r';', lambda match: ('PONTO_E_VIRGULA', ';')),
        (r',', lambda match: ('VIRGULA', ',')),
        (r'//.*', lambda match: ('COMENTARIO_LINHA', match.group(0))),  # Comentários de linha
        (r'{.*?}', lambda match: ('COMENTARIO_BLOCO', match.group(0))),  # Comentários de bloco
        (r'\s+', None),  # Ignora espaços em branco
    ]

    # Compila as expressões regulares
    regex_compiladas = [(re.compile(padrao), acao) for padrao, acao in regex_tokens]

    # Processamento da expressão
    posicao = 0
    tamanho = len(expressao)

    while posicao < tamanho:
        match = None
        for regex, acao in regex_compiladas:
            match = regex.match(expressao, posicao)
            if match:
                if acao:
                    lexema = match.group(0)
                    col_ini = posicao + 1
                    col_fim = posicao + len(lexema)
                    token_type, valor = acao(match)
                    tokens_encontrados.append({
                        'lexema': lexema,
                        'token': token_type,
                        'erro': '',
                        'linha': linha,
                        'col_ini': col_ini,
                        'col_fim': col_fim
                    })
                break

        if not match:
            # Caractere desconhecido
            lexema = expressao[posicao]
            col_ini = posicao + 1
            col_fim = col_ini
            tokens_encontrados.append({
                'lexema': lexema,
                'token': 'DESCONHECIDO',
                'erro': 'Caractere não reconhecido.',
                'linha': linha,
                'col_ini': col_ini,
                'col_fim': col_fim
            })
            posicao += 1
        else:
            posicao = match.end()

        # Atualiza a contagem de linhas
        if '\n' in expressao[posicao:]:
            linha += expressao[posicao:].count('\n')

    return tokens_encontrados

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
    
    # Realiza a análise léxica
    tokens = analisar_expressao(expressao)
    
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
# ------------------------------------------------------------------------------
# 4. Criação do Menu
# ------------------------------------------------------------------------------
def criar_menu(root, text_area, tree, text_log):
    """Cria a barra de menu e adiciona ao root."""
    menubar = tk.Menu(root)

    # Menu "Arquivo"
    menu_arquivo = tk.Menu(menubar, tearoff=False)
    menu_arquivo.add_command(label="Novo")
    menu_arquivo.add_command(label="Abrir", command=lambda: abrir_arquivo(text_area))
    menu_arquivo.add_command(label="Salvar")
    menu_arquivo.add_separator()
    menu_arquivo.add_command(label="Sair", command=root.quit)
    menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

    # Menu "Editar"
    menu_editar = tk.Menu(menubar, tearoff=False)
    menu_editar.add_command(label="Desfazer")
    menu_editar.add_command(label="Refazer")
    menubar.add_cascade(label="Editar", menu=menu_editar)

    # Menu "Exibir"
    menu_exibir = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Exibir", menu=menu_exibir)

    # Menu "Localizar"
    menu_localizar = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Localizar", menu=menu_localizar)

    # Menu "Compiler"
    menu_compiler = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Compiler", menu=menu_compiler)

    # Menu "Executar" - faz a análise e preenche a tabela
    # Menu "Executar" - faz a análise e preenche a tabela
    menu_executar = tk.Menu(menubar, tearoff=False)
    menu_executar.add_command(
        label="Executar Análise",
        command=lambda: executar_analise(text_area, tree, text_log)
    )
    menubar.add_cascade(label="Executar", menu=menu_executar)
    

    # Menu "Ajuda"
    menu_ajuda = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

    # Atribui a barra de menus à janela principal
    root.config(menu=menubar)

# ------------------------------------------------------------------------------
# 5. Abertura de Arquivo (para carregar texto no editor)
# ------------------------------------------------------------------------------
def abrir_arquivo(text_area):
    """Abre um arquivo de texto e carrega o conteúdo na área de texto."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", conteudo)
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")

# ------------------------------------------------------------------------------
# 6. Criação da área principal de texto
# ------------------------------------------------------------------------------
def criar_area_principal(root):
    """Cria a área principal (como um editor de texto) e a posiciona na janela."""
     # Frame para conter o contador e o texto
    frame_texto = ttk.Frame(root)
    frame_texto.grid(row=0, column=0, sticky="nsew")
    frame_texto.columnconfigure(1, weight=1)  # Área principal expande
    
    # Widget do contador de linhas (Text com fundo cinza)
    text_line_numbers = tk.Text(
        frame_texto,
        width=2,
        bg="#f0f0f0",
        bd=0,
        highlightthickness=0,
        state='disabled'
    )
    text_line_numbers.grid(row=0, column=0, sticky="ns")
    
    # Área principal de texto
    text_area = tk.Text(frame_texto)
    text_area.grid(row=0, column=1, sticky="nsew")
    
    # Sincroniza a rolagem vertical
    def sync_scroll(*args):
        text_line_numbers.yview_moveto(args[0])
        text_area.yview_moveto(args[0])
    
    vsb = ttk.Scrollbar(frame_texto, orient="vertical", command=sync_scroll)
    text_area.config(yscrollcommand=vsb.set)
    text_line_numbers.config(yscrollcommand=vsb.set)
    vsb.grid(row=0, column=2, sticky="ns")
    
    # Função para atualizar os números de linha
    def update_line_numbers(event=None):
        text_line_numbers.config(state='normal')
        text_line_numbers.delete('1.0', tk.END)
        
        # Obtém o número de linhas
        num_lines = text_area.index(tk.END).split('.')[0]
        line_numbers = '\n'.join(str(i) for i in range(1, int(num_lines)+1))
        
        text_line_numbers.insert('1.0', line_numbers)
        text_line_numbers.config(state='disabled')
    
    # Vincula eventos que modificam o texto
    text_area.bind('<Key>', update_line_numbers)
    text_area.bind('<MouseWheel>', update_line_numbers)
    text_area.bind('<Button-4>', update_line_numbers)
    text_area.bind('<Button-5>', update_line_numbers)
    text_area.bind('<FocusIn>', update_line_numbers)
    text_area.bind('<FocusOut>', update_line_numbers)
    
    # Atualiza inicialmente
    update_line_numbers()
    
    return text_area

# ------------------------------------------------------------------------------
# 7. Criação do bloco inferior com Notebook (duas abas)
# ------------------------------------------------------------------------------
def criar_bloco_inferior(root):
    """Cria o bloco inferior com abas. Retorna o Treeview da aba 'Tabela de Lexemas' e o Text do Log."""
    notebook = ttk.Notebook(root)
    notebook.grid(row=1, column=0, sticky="nsew")

    # Frame para "Log de Compilação"
    frame_log = ttk.Frame(notebook)
    text_log = tk.Text(frame_log)
    text_log.pack(expand=True, fill="both")
    notebook.add(frame_log, text="Log de Compilação")

    # Frame para "Tabela de Lexemas"
    frame_lexemas = ttk.Frame(notebook)
    colunas = ("Lexema", "Token", "Erro", "Linha", "ColIni", "ColFim")
    tree_lexemas = ttk.Treeview(frame_lexemas, columns=colunas, show="headings", height=8)
    
    # Configura o heading (título das colunas)
    for col in colunas:
        tree_lexemas.heading(col, text=col)
        tree_lexemas.column(col, width=100)
    
    tree_lexemas.pack(expand=True, fill="both")
    notebook.add(frame_lexemas, text="Tabela de Lexemas")
    
    return tree_lexemas, text_log
# ------------------------------------------------------------------------------
# 8. Função principal (main)
# ------------------------------------------------------------------------------
def main():
    # Cria a janela principal
    root = criar_janela_principal()

    # Cria a área de texto
    text_area = criar_area_principal(root)

    # Cria as abas inferiores e obtém o Treeview e o Text do Log
    tree_lexemas, text_log = criar_bloco_inferior(root)

    # Cria o menu (inclui a opção de "Executar" que faz a análise léxica)
    criar_menu(root, text_area, tree_lexemas, text_log)

    # Inicia o loop principal
    root.mainloop()

if __name__ == "__main__":
    main()