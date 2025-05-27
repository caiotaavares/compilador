# from compiler.symbol_table import SymbolTable

# ------------------------------------------------------------------------------
# ANALISADOR SINTÁTICO
# ------------------------------------------------------------------------------
# decl_var → var lista_decl_var
# lista_decl_var → tipo : lista_id ; lista_decl_var | ε
# tipo → int | boolean
# lista_id → id lista_id_tail
# lista_id_tail → , id lista_id_tail | ε
# ------------------------------------------------------------------------------
# ########## TABELA SINTÁTICA ##########
# | Não-Terminal      | PALAVRA_RESERVADA_VAR           | IDENTIFICADOR                                         | PALAVRA_RESERVADA_INT   | PALAVRA_RESERVADA_BOOLEAN  | SEPARADOR (`:`)    | PONTO_E_VIRGULA (`;`)     | `$`                   |
# |-------------------|---------------------------------|-------------------------------------------------------|-------------------------|----------------------------|--------------------|---------------------------|-----------------------|
# | **decl_var**      | decl_var → var lista_decl_var   | -                                                     | -                       | -                          | -                  | -                         | -                     |
# | **lista_decl_var**| -                               | lista_decl_var → lista_id : tipo ; lista_decl_var     | -                       | -                          | -                  | -                         | lista_decl_var → ε    |
# | **lista_id**      | -                               | lista_id → id lista_id_tail                           | -                       | -                          | -                  | -                         | -                     |
# | **lista_id_tail** | -                               | -                                                     | -                       | -                          | lista_id_tail → ε  | -                         | -                     |
# |                   | -                               | -                                                     | -                       | -                          | -                  | -                         | -                     |
# |                   | -                               | lista_id_tail → , id lista_id_tail                    | -                       | -                          | -                  | -                         | -                     |
# | **tipo**          | -                               | -                                                     | tipo → int              | tipo → boolean             | -                  | -                         | -                     |

# ------------------------------------------------------------------------------

# dicionário em Python, onde a chave é o símbolo não terminal e o valor é outro dicionário
tabela_sintatica = {
    # Diz que se o topo da pilha for decl_var e o próximo token for var, então 
    # deve expandir decl_var por essa produção.
    # -->
    # Chave externa = não-terminal.
    # Chave interna = token da entrada.
    # Valor = lista de símbolos da produção
    # --> 
    'programa': {
        'PALAVRA_RESERVADA_PROGRAM': [
            'PALAVRA_RESERVADA_PROGRAM', 'IDENTIFICADOR', 'PONTO_E_VIRGULA',
            'lista_decl_var', 'lista_procedimentos', 'bloco'
        ]
    },
    'lista_decl_var': {
        'PALAVRA_RESERVADA_INT': ['tipo', 'lista_id', 'PONTO_E_VIRGULA', 'lista_decl_var'],
        'PALAVRA_RESERVADA_BOOLEAN': ['tipo', 'lista_id', 'PONTO_E_VIRGULA', 'lista_decl_var'],
        'PALAVRA_RESERVADA_PROCEDURE': ['ε'],
        'PALAVRA_RESERVADA_BEGIN': ['ε'],
        '$': ['ε']
    },
    'lista_procedimentos': {
        'PALAVRA_RESERVADA_PROCEDURE': ['procedimento', 'lista_procedimentos'],
        'PALAVRA_RESERVADA_BEGIN': ['ε'],
        '$': ['ε']
    },
    'procedimento': {
        'PALAVRA_RESERVADA_PROCEDURE': [
            'PALAVRA_RESERVADA_PROCEDURE', 'IDENTIFICADOR', 'ABRE_PARENTESES', 'parametros',
            'FECHA_PARENTESES', 'PONTO_E_VIRGULA', 'lista_decl_var', 'bloco'
        ]
    },
    'parametros': {
        'PALAVRA_RESERVADA_VAR': ['PALAVRA_RESERVADA_VAR', 'IDENTIFICADOR', 'SEPARADOR', 'tipo']
    },
    'tipo': {
        'PALAVRA_RESERVADA_INT': ['PALAVRA_RESERVADA_INT'],
        'PALAVRA_RESERVADA_BOOLEAN': ['PALAVRA_RESERVADA_BOOLEAN']
    },
    'lista_id': {
        'IDENTIFICADOR': ['IDENTIFICADOR', 'lista_id_tail']
    },
    'lista_id_tail': {
        'VIRGULA': ['VIRGULA', 'IDENTIFICADOR', 'lista_id_tail'],
        'PONTO_E_VIRGULA': ['ε']
    },
    'bloco': {
        'PALAVRA_RESERVADA_BEGIN': ['PALAVRA_RESERVADA_BEGIN', 'comandos', 'PALAVRA_RESERVADA_END', 'PONTO_E_VIRGULA']
    },
    'comandos': {
        'IDENTIFICADOR': ['comando', 'comandos'],
        'PALAVRA_RESERVADA_IF': ['comando', 'comandos'],
        'PALAVRA_RESERVADA_END': ['ε']
    },
    'comando': {
        'IDENTIFICADOR': ['atribuicao'],
        'PALAVRA_RESERVADA_IF': ['condicional']
    },
    'atribuicao': {
        'IDENTIFICADOR': ['IDENTIFICADOR', 'ATRIBUICAO', 'expressao', 'PONTO_E_VIRGULA']
    },
    'condicional': {
        'PALAVRA_RESERVADA_IF': ['PALAVRA_RESERVADA_IF', 'ABRE_PARENTESES', 'expressao', 'FECHA_PARENTESES', 'comando']
    },
    'expressao': {
        'IDENTIFICADOR': ['termo', 'expressao_opcional'],
        'NUMERO_INTEIRO': ['termo', 'expressao_opcional'],
        'PALAVRA_RESERVADA_TRUE': ['termo', 'expressao_opcional'],
        'PALAVRA_RESERVADA_FALSE': ['termo', 'expressao_opcional'],
        'ABRE_PARENTESES': ['termo', 'expressao_tail'],
        'OPERADOR_SOMA': ['termo', 'expressao_tail'],  # Para operador unário +/-
        'OPERADOR_SUBTRACAO': ['termo', 'expressao_tail'],  # Para operador unário +/-
    },
    'expressao_tail': {
        'OPERADOR_SOMA': ['operador_soma', 'termo', 'expressao_tail'],
        'PONTO_E_VIRGULA': ['ε'],
        'FECHA_PARENTESES': ['ε'],
        'VIRGULA': ['ε'],
    },
    'termo': {
        'NUMERO_INTEIRO': ['NUMERO_INTEIRO'],
        'OPERADOR_SUBTRACAO': ['OPERADOR_SUBTRACAO', 'NUMERO_INTEIRO'],
        'OPERADOR_SOMA': ['OPERADOR_SOMA', 'NUMERO_INTEIRO'],
        'IDENTIFICADOR': ['IDENTIFICADOR'],
        'PALAVRA_RESERVADA_TRUE': ['fator', 'termo_tail'],
        'PALAVRA_RESERVADA_FALSE': ['fator', 'termo_tail'],
        'ABRE_PARENTESES': ['fator', 'termo_tail'],
    },
    'termo_tail': {
        'OPERADOR_MULTIPLICACAO': ['operador_multiplicacao', 'fator', 'termo_tail'],
        'OPERADOR_DIVISAO': ['operador_multiplicacao', 'fator', 'termo_tail'],
        'PALAVRA_RESERVADA_DIV': ['operador_multiplicacao', 'fator', 'termo_tail'],
        'OPERADOR_SOMA': ['ε'],
        'PONTO_E_VIRGULA': ['ε'],
        'FECHA_PARENTESES': ['ε'],
        'VIRGULA': ['ε'],
    },
    'fator': {
        'OPERADOR_SOMA': ['OPERADOR_UNARIO', 'fator'],
        'OPERADOR_SUBTRACAO': ['OPERADOR_UNARIO', 'fator'],
        'IDENTIFICADOR': ['IDENTIFICADOR'],
        'NUMERO_INTEIRO': ['NUMERO_INTEIRO'],
        'PALAVRA_RESERVADA_TRUE': ['PALAVRA_RESERVADA_TRUE'],
        'PALAVRA_RESERVADA_FALSE': ['PALAVRA_RESERVADA_FALSE'],
        'ABRE_PARENTESES': ['ABRE_PARENTESES', 'expressao', 'FECHA_PARENTESES'],
    },
    'operador_soma': {
        'OPERADOR_SOMA': ['OPERADOR_SOMA'],
        'OPERADOR_SUBTRACAO': ['OPERADOR_SUBTRACAO'],
    },
    'operador_multiplicacao': {
        'OPERADOR_MULTIPLICACAO': ['OPERADOR_MULTIPLICACAO'],
        'OPERADOR_DIVISAO': ['OPERADOR_DIVISAO'],
        'PALAVRA_RESERVADA_DIV': ['PALAVRA_RESERVADA_DIV'],
    },
    'expressao_opcional': {
        'MENOR': ['operador_relacional', 'termo'],
        'MAIOR': ['operador_relacional', 'termo'],
        'IGUALDADE': ['operador_relacional', 'termo'],
        'MAIOR_IGUAL': ['operador_relacional', 'termo'],
        'MENOR_IGUAL': ['operador_relacional', 'termo'],
        'DIFERENTE': ['operador_relacional', 'termo'],
        'PONTO_E_VIRGULA': ['ε']  # quando não há operador (ex: a := 1;)
    },
    'operador_relacional': {
        'MENOR': ['MENOR'],
        'MAIOR': ['MAIOR'],
        'IGUALDADE': ['IGUALDADE'],
        'DIFERENTE': ['DIFERENTE'],
        'MAIOR_IGUAL': ['MAIOR_IGUAL'],
        'MENOR_IGUAL': ['MENOR_IGUAL']
    },
    'chamada_procedimento': {
        'IDENTIFICADOR': ['IDENTIFICADOR', 'ABRE_PARENTESES', 'lista_argumentos', 'FECHA_PARENTESES', 'PONTO_E_VIRGULA']
    },
    'lista_argumentos': {
        'IDENTIFICADOR': ['expressao', 'lista_argumentos_tail'],
        'NUMERO_INTEIRO': ['expressao', 'lista_argumentos_tail'],
        'PALAVRA_RESERVADA_TRUE': ['expressao', 'lista_argumentos_tail'],
        'PALAVRA_RESERVADA_FALSE': ['expressao', 'lista_argumentos_tail'],
        'ABRE_PARENTESES': ['expressao', 'lista_argumentos_tail'],
        'OPERADOR_SOMA': ['expressao', 'lista_argumentos_tail'],
        'OPERADOR_SUBTRACAO': ['expressao', 'lista_argumentos_tail'],
        '$': ['ε'],
        'FECHA_PARENTESES': ['ε'],
    },
    'lista_argumentos_tail': {
        'VIRGULA': ['VIRGULA', 'expressao', 'lista_argumentos_tail'],
        'FECHA_PARENTESES': ['ε'],
    },
}

def analisar_declaracoes(tokens):
    pilha = ['$', 'programa']
    pos = 0
    tamanho = len(tokens)

    sync_tokens = {
        'decl_var': ['PALAVRA_RESERVADA_BEGIN', 'PALAVRA_RESERVADA_PROCEDURE', '$'],
        'lista_decl_var': ['PALAVRA_RESERVADA_BEGIN', 'PALAVRA_RESERVADA_PROCEDURE', '$'],
        'tipo': ['SEPARADOR', 'PONTO_E_VIRGULA', 'PALAVRA_RESERVADA_BEGIN', '$'],
        'lista_id': ['PONTO_E_VIRGULA', 'PALAVRA_RESERVADA_BEGIN', 'PALAVRA_RESERVADA_PROCEDURE', '$'],
        'lista_id_tail': ['PONTO_E_VIRGULA', 'PALAVRA_RESERVADA_BEGIN', 'PALAVRA_RESERVADA_PROCEDURE', '$'],
    }
    
    sync_tokens.update({
        'atribuicao': ['PONTO_E_VIRGULA'],
        'expressao': ['PONTO_E_VIRGULA', 'FECHA_PARENTESES'],
        'comando': ['PONTO_E_VIRGULA', 'PALAVRA_RESERVADA_END', 'PALAVRA_RESERVADA_IF', 'IDENTIFICADOR'],
        'condicional': ['PONTO_E_VIRGULA', 'PALAVRA_RESERVADA_END', 'PALAVRA_RESERVADA_IF', 'IDENTIFICADOR'],
    })

    erros = []

    def token_atual():
        # Protege para não sair do índice
        if pos < tamanho:
            return tokens[pos]['token']
        return '$'

    def lexema_atual():
        if pos < tamanho:
            return tokens[pos]['lexema']
        return 'EOF'

    def linha_atual():
        if pos < tamanho:
            return tokens[pos]['linha']
        return -1

    while pilha:
        topo = pilha.pop()

        atual = token_atual()

        if topo == 'ε':
            continue

        if topo == atual:
            pos += 1

            # Se passou do fim, para o loop
            if pos > tamanho:
                break

        elif topo in tabela_sintatica:
            producao = tabela_sintatica[topo].get(atual)

            if producao:
                for simbolo in reversed(producao):
                    if simbolo != 'ε':
                        pilha.append(simbolo)
            else:
                erros.append(f"Erro sintático: token inesperado '{lexema_atual()}' na linha {linha_atual()}. Tentando recuperação...")

                sync_set = sync_tokens.get(topo, ['$'])
                # Enquanto token atual não for sincronizador e não fim da entrada
                while atual not in sync_set and atual != '$':
                    pos += 1
                    atual = token_atual()
                # Se chegou no fim, sai do loop
                if atual == '$':
                    break

                # Não empilha nada para tentar continuar após sincronizar

        else:
            # topo é terminal mas diferente do atual (erro)
            erros.append(f"Erro sintático: token inesperado '{lexema_atual()}' na linha {linha_atual()}. Esperava '{topo}'. Tentando sincronizar...")

            # Descarta token atual para tentar sincronizar
            pos += 1

            # Se passou do fim, para o loop
            if pos > tamanho:
                break

            # Não empilha nada, tenta continuar

    if erros:
        raise SyntaxError('\n'.join(erros))

    return True
