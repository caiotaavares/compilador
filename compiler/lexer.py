# ------------------------------------------------------------------------------
# 1. Função de análise léxica
# ------------------------------------------------------------------------------
import re

def analisar_expressao(expressao):
    """Faz uma análise léxica completa da expressão usando regex."""
    tokens_encontrados = []
    linha = 1  # começa na linha 1
    posicao = 0
    tamanho = len(expressao)

    # Definição das expressões regulares
    regex_tokens = [
        (r'\b(program|begin|if|then|else|while|do|procedure|var|int|boolean|true|false|read|write)\b', lambda match: ('PALAVRA_RESERVADA_' + match.group(0).upper(), match.group(0))),
        (r'\bend\b', lambda match: ('PALAVRA_RESERVADA_END', 'end')),
        (r'\.', lambda match: ('PONTO', '.')),
        (r'\bdiv\b', lambda match: ('OPERADOR_DIV', 'div')),
        (r'[a-zA-Z_][a-zA-Z0-9_]*', lambda match: validar_identificador(match)),
        (r'\d+(\.\d+)?', lambda match: validar_numero(match)),
        (r':=', lambda match: ('ATRIBUICAO', ':=')),
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
        (r';', lambda match: ('PONTO_E_VIRGULA', ';')),
        (r',', lambda match: ('VIRGULA', ',')),
        (r'//.*', lambda match: ('COMENTARIO_LINHA', match.group(0))),  # Comentários de linha
        (r'{.*?}', lambda match: ('COMENTARIO_BLOCO', match.group(0))),  # Comentários de bloco
        (r'\s+', None),  # Ignora espaços em branco
    ]

    # Compila as expressões regulares
    regex_compilados = [(re.compile(padrao), acao) for padrao, acao in regex_tokens]

    ## Itera expressao para cada regex compilado
    while posicao < tamanho:
        match = None
        for regex, acao in regex_compilados:
            match = regex.match(expressao, posicao)
            if match:
                if acao:
                    lexema = match.group(0)
                    # comentário bloco (atualiza linha e pula)
                    if lexema.startswith('{'):
                        fechamento = expressao.find('}', posicao)
                        if fechamento == -1:
                            linha_erro = linha + expressao.count('\n', posicao)
                            raise SyntaxError(f"Erro: comentário de bloco '{{' iniciado na linha {linha_erro} sem fechamento '}}'.")
                        linha += lexema.count('\n')
                        posicao = fechamento + 1
                        break

                    # comentário linha
                    if lexema.startswith('//'):
                        linha += lexema.count('\n')
                        posicao = match.end()
                        break

                    col_ini = posicao + 1
                    col_fim = posicao + len(lexema)
                    token_type, valor = acao(match)
                    erro = ''
                    if token_type == 'NUMERO_INVALIDO':
                        erro = 'Número excede limite (int32).'
                    elif token_type == 'IDENTIFICADOR_INVALIDO':
                        erro = 'Identificador excede 30 caracteres.'

                    tokens_encontrados.append({
                        'lexema': lexema,
                        'token': token_type,
                        'erro': erro,
                        'linha': linha,
                        'col_ini': col_ini,
                        'col_fim': col_fim
                    })

                    # ATUALIZA LINHA IMEDIATAMENTE APÓS CONSUMIR TOKEN:
                    trecho = expressao[posicao:match.end()]
                    linha += trecho.count('\n')
                    posicao = match.end()
                else:
                    # ação None para espaços, só pula
                    trecho = expressao[posicao:match.end()]
                    linha += trecho.count('\n')
                    posicao = match.end()
                break

        if not match:
            lexema = expressao[posicao]
            tokens_encontrados.append({
                'lexema': lexema,
                'token': 'DESCONHECIDO',
                'erro': 'Caractere não reconhecido.',
                'linha': linha,
                'col_ini': posicao + 1,
                'col_fim': posicao + 1
            })
            posicao += 1

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