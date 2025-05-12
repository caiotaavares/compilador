from compiler.symbol_table import SymbolTable

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
    'decl_var': {
        'PALAVRA_RESERVADA_VAR': ['PALAVRA_RESERVADA_VAR', 'lista_decl_var']
    },
    'lista_decl_var': {
        'PALAVRA_RESERVADA_INT': ['tipo', 'SEPARADOR', 'lista_id', 'PONTO_E_VIRGULA', 'lista_decl_var'],
        'PALAVRA_RESERVADA_BOOLEAN': ['tipo', 'SEPARADOR', 'lista_id', 'PONTO_E_VIRGULA', 'lista_decl_var'],
        '$': ['ε'],
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
        'PONTO_E_VIRGULA': ['ε'],
    }
}


def analisar_declaracoes(tokens):
    # Pilha inicial da análise sintática
    # Começa com $ (fim da entrada) e o símbolo inicial da gramática (decl_var)
    pilha = ['$', 'decl_var']

    pos = 0  # posição atual no vetor de tokens
    tamanho = len(tokens)  # número total de tokens
    
    def token_atual():
        # Retorna o tipo do token atual ou $ se chegou ao fim
        if pos < tamanho:
            return tokens[pos]['token']
        return '$'
    
    def lexema_atual():
        # Retorna o lexema atual (apenas para mensagens de erro)
        if pos < tamanho:
            return tokens[pos]['lexema']
        return 'EOF'
    
    while pilha:
        topo = pilha.pop()  # Remove o topo da pilha
        atual = token_atual()  # Lê o token atual da entrada
        
        if topo == 'ε':
            continue

        if topo == atual:
            pos += 1  # casou terminal, consome token
        elif topo in tabela_sintatica:
            producao = tabela_sintatica[topo].get(atual)
            if producao:
                # Adiciona a produção na pilha
                for simbolo in reversed(producao):
                    if simbolo != 'ε':
                        pilha.append(simbolo)
        else:
            raise SyntaxError(f"Erro de sintaxe: token inesperado '{lexema_atual()}' na linha {tokens[pos]['linha']}")
    return True
