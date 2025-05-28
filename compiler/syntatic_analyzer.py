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
# | Não-Terminal      | PALAVRA_RESERVADA_VAR           | IDENTIFICADOR                                         | PALAVRA_RESERVADA_INT   | PALAVRA_RESERVADA_BOOLEAN  | SEPARADOR (:)    | PONTO_E_VIRGULA (;)     | $                   |
# |-------------------|---------------------------------|-------------------------------------------------------|-------------------------|----------------------------|--------------------|---------------------------|-----------------------|
# | *decl_var*      | decl_var → var lista_decl_var   | -                                                     | -                       | -                          | -                  | -                         | -                     |
# | *lista_decl_var*| -                               | lista_decl_var → lista_id : tipo ; lista_decl_var     | -                       | -                          | -                  | -                         | lista_decl_var → ε    |
# | *lista_id*      | -                               | lista_id → id lista_id_tail                           | -                       | -                          | -                  | -                         | -                     |
# | *lista_id_tail* | -                               | -                                                     | -                       | -                          | lista_id_tail → ε  | -                         | -                     |
# |                   | -                               | -                                                     | -                       | -                          | -                  | -                         | -                     |
# |                   | -                               | lista_id_tail → , id lista_id_tail                    | -                       | -                          | -                  | -                         | -                     |
# | *tipo*          | -                               | -                                                     | tipo → int              | tipo → boolean             | -                  | -                         | -                     |

# ------------------------------------------------------------------------------

# Tabela sintática LL(1) para a linguagem LALG
# dicionário em Python, onde a chave é o símbolo não terminal e o valor é outro dicionário
tabela_sintatica = {
    'programa': {
        'PALAVRA_RESERVADA_PROGRAM': [
            'PALAVRA_RESERVADA_PROGRAM', 'IDENTIFICADOR', 'PONTO_E_VIRGULA', 'decl_var', 'bloco_final'
        ]
    },
    'decl_var': {
        'PALAVRA_RESERVADA_INT': ['tipo', 'lista_id', 'PONTO_E_VIRGULA', 'decl_var'],
        'PALAVRA_RESERVADA_BOOLEAN': ['tipo', 'lista_id', 'PONTO_E_VIRGULA', 'decl_var'],
        'PALAVRA_RESERVADA_BEGIN': ['ε']
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
    
    # Estrutura básica (Bloco principal)
    'bloco_final': {
        'PALAVRA_RESERVADA_BEGIN': ['PALAVRA_RESERVADA_BEGIN', 'comandos', 'PALAVRA_RESERVADA_END_PONTO']
    },
    
    # Chamada de procedimentos dentro do begin... end. principal
    # program exemplo;
    # ...
    
    # begin
    #   <ESSA PARTE>
    # end.
    'comandos': {
        'IDENTIFICADOR': ['comando', 'PONTO_E_VIRGULA', 'comandos'],
        'PALAVRA_RESERVADA_READ': ['comando', 'PONTO_E_VIRGULA', 'comandos'],
        'PALAVRA_RESERVADA_WRITE': ['comando', 'PONTO_E_VIRGULA', 'comandos'],
        'PALAVRA_RESERVADA_IF': ['comando','comandos'],
        'PALAVRA_RESERVADA_WHILE': ['comando', 'PONTO_E_VIRGULA', 'comandos'],
        'PALAVRA_RESERVADA_BEGIN': ['comando', 'PONTO_E_VIRGULA', 'comandos'],
        'PALAVRA_RESERVADA_END': ['ε'],
        'PALAVRA_RESERVADA_END_PONTO': ['ε']
    },
    'comando': {
        'IDENTIFICADOR': ['atribuicao_ou_chamada'],
        'PALAVRA_RESERVADA_READ': ['leitura'],
        'PALAVRA_RESERVADA_WRITE': ['escrita'],
        'PALAVRA_RESERVADA_IF': ['condicional'],
        'PALAVRA_RESERVADA_WHILE': ['repeticao'],
        'PALAVRA_RESERVADA_BEGIN': ['bloco']
    },
    'atribuicao_ou_chamada': {
        'IDENTIFICADOR': ['IDENTIFICADOR', 'atribuicao_ou_chamada_tail']
    },
    'atribuicao_ou_chamada_tail': {
        'ATRIBUICAO': ['ATRIBUICAO', 'expressao'],
        'ABRE_PARENTESES': ['ABRE_PARENTESES', 'IDENTIFICADOR', 'FECHA_PARENTESES']
    },
    'leitura': {
        'PALAVRA_RESERVADA_READ': ['PALAVRA_RESERVADA_READ', 'ABRE_PARENTESES', 'IDENTIFICADOR', 'FECHA_PARENTESES']
    },
    'escrita': {
        'PALAVRA_RESERVADA_WRITE': ['PALAVRA_RESERVADA_WRITE', 'ABRE_PARENTESES', 'IDENTIFICADOR', 'FECHA_PARENTESES']
    },
    'condicional': {
        'PALAVRA_RESERVADA_IF': [
            'PALAVRA_RESERVADA_IF',
            'ABRE_PARENTESES', 'expressao', 'FECHA_PARENTESES',
            # 'PALAVRA_RESERVADA_THEN',
            'comando',
            'cond_else'
        ]
    },
    'cond_else': {
        'PALAVRA_RESERVADA_ELSE': ['PALAVRA_RESERVADA_ELSE', 'comando'],
        'PALAVRA_RESERVADA_END': ['ε'],
        # 'PONTO_E_VIRGULA': ['ε'],
        '$': ['ε']
    },
    'repeticao': {
        'PALAVRA_RESERVADA_WHILE': ['PALAVRA_RESERVADA_WHILE', 'ABRE_PARENTESES', 'expressao', 'FECHA_PARENTESES', 'comando']
    },
    'bloco': {
        'PALAVRA_RESERVADA_BEGIN': ['PALAVRA_RESERVADA_BEGIN', 'comandos', 'PALAVRA_RESERVADA_END']
    },
    'expressao': {
        'IDENTIFICADOR': ['termo', 'expressao_tail'],
        'NUMERO_INTEIRO': ['termo', 'expressao_tail'],
        'NUMERO_REAL': ['termo', 'expressao_tail'],
        'OPERADOR_SOMA': ['OPERADOR_SOMA', 'termo', 'expressao_tail'],
        'OPERADOR_SUBTRACAO': ['OPERADOR_SUBTRACAO', 'termo', 'expressao_tail'],
        'PALAVRA_RESERVADA_TRUE': ['termo', 'expressao_tail'],
        'PALAVRA_RESERVADA_FALSE': ['termo', 'expressao_tail'],
        'ABRE_PARENTESES': ['termo', 'expressao_tail']
    },
    'expressao_tail': {
        'OPERADOR_SOMA': ['OPERADOR_SOMA', 'termo', 'expressao_tail'],
        'OPERADOR_SUBTRACAO': ['OPERADOR_SUBTRACAO', 'termo', 'expressao_tail'],
        'OPERADOR_MULTIPLICACAO': ['OPERADOR_MULTIPLICACAO', 'termo', 'expressao_tail'],
        'OPERADOR_DIV': ['OPERADOR_DIV', 'termo', 'expressao_tail'],
        'MENOR': ['MENOR', 'termo', 'expressao_tail'],
        'MAIOR': ['MAIOR', 'termo', 'expressao_tail'],
        'MENOR_IGUAL': ['MENOR_IGUAL', 'termo', 'expressao_tail'],
        'MAIOR_IGUAL': ['MAIOR_IGUAL', 'termo', 'expressao_tail'],
        'IGUALDADE': ['IGUALDADE', 'termo', 'expressao_tail'],
        'DIFERENTE': ['DIFERENTE', 'termo', 'expressao_tail'],
        'FECHA_PARENTESES': ['ε'],
        'PONTO_E_VIRGULA': ['ε'],
        # 'PALAVRA_RESERVADA_THEN': ['ε'],
        'PALAVRA_RESERVADA_DO': ['ε'],
        'PALAVRA_RESERVADA_END': ['ε'],
        'PALAVRA_RESERVADA_ELSE': ['ε']
    },
    'termo': {
        'IDENTIFICADOR': ['IDENTIFICADOR'],
        'NUMERO_INTEIRO': ['NUMERO_INTEIRO'],
        'NUMERO_REAL': ['NUMERO_REAL'],
        'PALAVRA_RESERVADA_TRUE': ['PALAVRA_RESERVADA_TRUE'],
        'PALAVRA_RESERVADA_FALSE': ['PALAVRA_RESERVADA_FALSE'],
        'OPERADOR_SOMA': ['OPERADOR_SOMA', 'termo'],
        'OPERADOR_SUBTRACAO': ['OPERADOR_SUBTRACAO', 'termo'],
        'ABRE_PARENTESES': ['ABRE_PARENTESES', 'expressao', 'FECHA_PARENTESES']
    }
}

print(tabela_sintatica)

def analisar_declaracoes(tokens):
    pilha = ['$', 'programa']
    pos = 0
    tamanho = len(tokens)
    
    print(tokens)

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
    
    sync_tokens.update({
        'bloco_programa': ['PONTO'],
        'bloco_procedure': ['PONTO_E_VIRGULA'],
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