import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def criar_janela_principal():
    """Cria a janela principal e retorna o objeto root."""
    root = tk.Tk()
    root.title("PCIDE - Calculadora/Lexer")
    root.geometry("800x600")

    # Configura o grid para redimensionamento
    root.rowconfigure(0, weight=3)  # Área de texto principal
    root.rowconfigure(1, weight=1)  # Aba inferior (tabela)
    root.columnconfigure(0, weight=1)

    return root

# ------------------------------------------------------------------------------
# 1. Função de análise léxica
# ------------------------------------------------------------------------------
def analisar_expressao(expressao):
    """
    Faz uma análise léxica simples da expressão.
    Retorna uma lista de dicionários com as chaves:
      - lexema
      - token
      - erro
      - linha
      - col_ini
      - col_fim
    """
    tokens_encontrados = []
    linha = 1  # Para simplificar, consideramos que tudo está na linha 1
    i = 0
    tamanho = len(expressao)

    while i < tamanho:
        char = expressao[i]

        # Ignora espaços em branco e quebras de linha
        if char in [' ', '\t', '\n', '\r']:
            if char == '\n':
                linha += 1
            i += 1
            continue

        # Se for dígito ou ponto, tentamos ler um número (int ou float)
        if char.isdigit() or (char == '.'):
            inicio = i
            ponto_encontrado = (char == '.')
            i += 1
 
            while i < tamanho:
                prox_char = expressao[i]
                # Se for dígito, continua
                if prox_char.isdigit():
                    i += 1
                # Se for ponto e ainda não encontramos ponto, continua
                elif prox_char == '.' and not ponto_encontrado:
                    ponto_encontrado = True
                    i += 1
                else:
                    # Se não for dígito nem ponto, paramos
                    break

            lexema = expressao[inicio:i]
            # Verifica se há mais de um ponto (caso simples de erro)
            if lexema.count('.') > 1:
                token_type = "DESCONHECIDO"
                erro = "Número inválido (múltiplos pontos)."
            else:
                if '.' in lexema:
                    token_type = "NUMERO_REAL"
                else:
                    token_type = "NUMERO_INTEIRO"
                erro = ""

            # Índice de colunas (iniciando em 1 para ficar mais intuitivo)
            col_ini = inicio + 1
            col_fim = i

            tokens_encontrados.append({
                'lexema': lexema,
                'token': token_type,
                'erro': erro,
                'linha': linha,
                'col_ini': col_ini,
                'col_fim': col_fim
            })

        # Se for um operador simples ou parêntese
        elif char in ['+', '-', '*', '/', '(', ')']:
            inicio = i
            i += 1

            # Índice de colunas
            col_ini = inicio + 1
            col_fim = i

            if char in ['+', '-', '*', '/']:
                if char == '+':
                    token_type = "OPERADOR_SOMA"
                if  char == '-':
                    token_type = "OPERADOR_SUBTRACAO"
                if  char == '*':
                    token_type = "OPERADOR_MULTIPLICACAO"
                if  char == '/':
                    token_type = "OPERADOR_DIVISAO"
                if  char == '(':
                    token_type = "OPERADOR_ABRE_CHAVES"
                if  char == ')':
                    token_type = "OPERADOR_FECHA_CHAVES"
                if  char == '[':
                    token_type = "OPERADOR_ABRE_COLCHETES"
                if  char == '[':
                    token_type = "OPERADOR_FECHA_COLCHETES"
            else:
                token_type = "PAREN"

            tokens_encontrados.append({
                'lexema': char,
                'token': token_type,
                'erro': "",
                'linha': linha,
                'col_ini': col_ini,
                'col_fim': col_fim
            })
        else:
            # Caracter desconhecido
            inicio = i
            i += 1

            col_ini = inicio + 1
            col_fim = i

            tokens_encontrados.append({
                'lexema': char,
                'token': "UNKNOWN",
                'erro': "Caractere não reconhecido.",
                'linha': linha,
                'col_ini': col_ini,
                'col_fim': col_fim
            })

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
        tree.insert("", "end", values=(
            t['lexema'],
            t['token'],
            t['erro'],
            t['linha'],
            t['col_ini'],
            t['col_fim']
        ))

# ------------------------------------------------------------------------------
# 3. Função de callback para o menu "Executar"
# ------------------------------------------------------------------------------
def executar_analise(text_area, tree):
    """
    Lê o texto da área principal, analisa e exibe o resultado na Tabela de Lexemas.
    """
    expressao = text_area.get("1.0", tk.END).strip()
    tokens = analisar_expressao(expressao)
    popular_tabela_lexemas(tree, tokens)

# ------------------------------------------------------------------------------
# 4. Criação do Menu
# ------------------------------------------------------------------------------
def criar_menu(root, text_area, tree):
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
    menu_executar = tk.Menu(menubar, tearoff=False)
    menu_executar.add_command(
        label="Executar Análise",
        command=lambda: executar_analise(text_area, tree)
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
    text_area = tk.Text(root)
    text_area.grid(row=0, column=0, sticky="nsew")
    return text_area

# ------------------------------------------------------------------------------
# 7. Criação do bloco inferior com Notebook (duas abas)
# ------------------------------------------------------------------------------
def criar_bloco_inferior(root):
    """Cria o bloco inferior com abas. Retorna o Treeview da aba 'Tabela de Lexemas'."""
    notebook = ttk.Notebook(root)
    notebook.grid(row=1, column=0, sticky="nsew")

    # Frame para "Log de Compilação"
    frame_log = ttk.Frame(notebook)
    text_log = tk.Text(frame_log)
    text_log.pack(expand=True, fill="both")
    notebook.add(frame_log, text="Log de Compilação")

    # Frame para "Tabela de Lexemas"
    frame_lexemas = ttk.Frame(notebook)
    # Criamos uma Treeview para exibir as colunas: Lexema, Token, Erro, Linha, ColIni, ColFim
    colunas = ("Lexema", "Token", "Erro", "Linha", "ColIni", "ColFim")
    tree_lexemas = ttk.Treeview(frame_lexemas, columns=colunas, show="headings", height=8)
    
    # Configura o heading (título das colunas)
    tree_lexemas.heading("Lexema", text="Lexema")
    tree_lexemas.heading("Token", text="Token")
    tree_lexemas.heading("Erro", text="Erro")
    tree_lexemas.heading("Linha", text="Linha")
    tree_lexemas.heading("ColIni", text="Col. Inicial")
    tree_lexemas.heading("ColFim", text="Col. Final")

    # Ajusta a largura de cada coluna (opcional)
    tree_lexemas.column("Lexema", width=100)
    tree_lexemas.column("Token", width=100)
    tree_lexemas.column("Erro", width=150)
    tree_lexemas.column("Linha", width=50)
    tree_lexemas.column("ColIni", width=80)
    tree_lexemas.column("ColFim", width=80)

    # Adiciona o Treeview ao frame
    tree_lexemas.pack(expand=True, fill="both")

    notebook.add(frame_lexemas, text="Tabela de Lexemas")

    return tree_lexemas

# ------------------------------------------------------------------------------
# 8. Função principal (main)
# ------------------------------------------------------------------------------
def main():
    # Cria a janela principal
    root = criar_janela_principal()

    # Cria a área de texto
    text_area = criar_area_principal(root)

    # Cria as abas inferiores e obtém o Treeview para a tabela de lexemas
    tree_lexemas = criar_bloco_inferior(root)

    # Cria o menu (inclui a opção de "Executar" que faz a análise léxica)
    criar_menu(root, text_area, tree_lexemas)

    # Inicia o loop principal
    root.mainloop()

if __name__ == "__main__":
    main()
