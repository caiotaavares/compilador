# ----------------------------------------------------------------------------
# Utils para análise semântica: construção e checagem de tabela de símbolos
# ----------------------------------------------------------------------------

def build_symbol_table(tokens):
    """
    Retorna um dict: nome → info ({ 'kind': 'var'|'proc'|'prog', 'type': <tipo opcional>, 'line': <linha> })
    """
    table = {}
    i = 0
    n = len(tokens)

    while i < n:
        t = tokens[i]

        # programa <IDENTIFICADOR>
        if t['token'] == 'PALAVRA_RESERVADA_PROGRAM':
            # o próximo token deve ser o nome do programa
            if i + 1 < n and tokens[i+1]['token'] == 'IDENTIFICADOR':
                prog_name = tokens[i+1]['lexema']
                table[prog_name] = { 'kind': 'prog', 'line': tokens[i+1]['linha'] }
                # pular 'program' e o identificador
                i += 2
                continue

        # declarações de variáveis: int/boolean
        if t['token'] in ('PALAVRA_RESERVADA_INT', 'PALAVRA_RESERVADA_BOOLEAN'):
            tipo = 'int' if t['token'].endswith('INT') else 'boolean'
            j = i + 1
            # lista de identificadores separados por vírgula
            while j < n and tokens[j]['token'] == 'IDENTIFICADOR':
                name = tokens[j]['lexema']
                table[name] = { 'kind': 'var', 'type': tipo, 'line': tokens[j]['linha'] }
                j += 1
                if j < n and tokens[j]['token'] == 'VIRGULA':
                    j += 1
                else:
                    break
            i = j
            continue

        # parâmetros formais: var x,y : tipo
        if t['token'] == 'PALAVRA_RESERVADA_VAR':
            j = i + 1
            while j < n and tokens[j]['token'] == 'IDENTIFICADOR':
                name = tokens[j]['lexema']
                table[name] = { 'kind': 'param', 'line': tokens[j]['linha'] }
                j += 1
                if j < n and tokens[j]['token'] == 'VIRGULA':
                    j += 1
                else:
                    break
            i = j
            continue

        # procedure <IDENTIFICADOR>
        if t['token'] == 'PALAVRA_RESERVADA_PROCEDURE':
            if i + 1 < n and tokens[i+1]['token'] == 'IDENTIFICADOR':
                name = tokens[i+1]['lexema']
                table[name] = { 'kind': 'proc', 'line': tokens[i+1]['linha'] }
            i += 1
            continue

        # caso nenhum, avançar
        i += 1

    return table


def check_semantics(tokens, symtab):
    """
    Retorna lista de mensagens de erro semântico para usos de identificadores não declarados.
    """
    erros = []

    for t in tokens:
        if t['token'] == 'IDENTIFICADOR':
            name = t['lexema']
            # se não estiver na tabela de símbolos, é erro
            if name not in symtab:
                erros.append(f"Erro semântico: '{name}' não declarado na linha {t['linha']}." )
    return erros
