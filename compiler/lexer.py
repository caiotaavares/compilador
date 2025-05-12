# ------------------------------------------------------------------------------
# 1. Função de análise léxica
# ------------------------------------------------------------------------------
import re

def analisar_expressao(expressao):
    """Faz uma análise léxica completa da expressão usando regex."""
    tokens_encontrados = []
    linha = 1  # Começa na linha 1

    # # Verificação de comentário de bloco não fechado
    # aberturas = [m.start() for m in re.finditer(r'\{', expressao)]
    # fechamentos = [m.start() for m in re.finditer(r'\}', expressao)]

    # if len(aberturas) != len(fechamentos):
    #     # Localiza a posição do erro (primeira abertura sem fechamento)
    #     if len(aberturas) > len(fechamentos):
    #         pos_erro = aberturas[len(fechamentos)]
    #         linha_erro = expressao.count('\n', 0, pos_erro) + 1
    #         raise SyntaxError(f"Erro: comentário de bloco '{{' iniciado na linha {linha_erro} não possui fechamento '}}'.")
    #     else:
    #         raise SyntaxError("Erro: comentário de bloco '}' sem abertura correspondente.")

    # # Limpeza dos comentários
    # expressao = re.sub(r'\{[^}]*\}', '', expressao, flags=re.DOTALL)  # Comentário de bloco
    # expressao = re.sub(r'//.*', '', expressao)  # Comentário de linha


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
        "write": "PALAVRA_RESERVADA_WRITE",
    }

    # Definição das expressões regulares
    regex_tokens = [
        (r'\b(program|begin|if|then|else|while|do|procedure|var|int|boolean|true|false|read|write)\b', lambda match: ('PALAVRA_RESERVADA_' + match.group(0).upper(), match.group(0))),
        (r'\bend\.', lambda match: ('PALAVRA_RESERVADA_END_PONTO', match.group(0))),
        (r'\bend\b', lambda match: ('PALAVRA_RESERVADA_END', match.group(0))),
        # (r'[a-zA-Z_][a-zA-Z0-9_]*', lambda match: ('IDENTIFICADOR', match.group(0))),
        (r'[a-zA-Z_][a-zA-Z0-9_]*', lambda match: validar_identificador(match)),
        # (r'\d+(\.\d+)?', lambda match: ('NUMERO_REAL' if '.' in match.group(0) else 'NUMERO_INTEIRO', match.group(0))),
        (r'\d+(\.\d+)?', lambda match: validar_numero(match)),
        (r':=', lambda match: ('ATRIBUICAO', '::=')),
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
                    # overflow
                    erro = ''
                    if token_type == 'NUMERO_INVALIDO':
                        erro = 'Número excede o limite permitido (int32).'
                    # identificador
                    elif token_type == 'IDENTIFICADOR_INVALIDO':
                        erro = 'Identificador excede o tamanho máximo permitido (30 caracteres).'
                
                    tokens_encontrados.append({
                        'lexema': lexema,
                        'token': token_type,
                        'erro': erro,
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

def validar_numero(match):
    lexema = match.group(0)
    try:
        if '.' in lexema:
            float(lexema)  # tenta converter para float
            return ('NUMERO_REAL', lexema)
        else:
            valor = int(lexema)
            if valor > 2**31 - 1:
                raise ValueError("Número inteiro excede o limite de 32 bits")
            return ('NUMERO_INTEIRO', lexema)
    except ValueError:
        return ('NUMERO_INVALIDO', lexema)

def validar_identificador(match, limite=30):
    lexema = match.group(0)
    if len(lexema) > limite:
        return ('IDENTIFICADOR_INVALIDO', lexema)
    return ('IDENTIFICADOR', lexema)
