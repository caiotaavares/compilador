# Tabela sintática LL(1) para a linguagem LALG
# dicionário em Python, onde a chave é o símbolo não terminal e o valor é outro dicionário

tabela_sintatica = {
    #### Programa e Bloco ####
    # 1. <programa> ::= program IDENTIFICADOR ; bloco .
    'programa': {
        'PALAVRA_RESERVADA_PROGRAM': [
            'PALAVRA_RESERVADA_PROGRAM', 'IDENTIFICADOR', 'PONTO_E_VIRGULA', 'bloco', 'PONTO'
        ]
    },

    # 2. <bloco> ::= [<parte_decl_var>] [<parte_decl_sub_rotinas>] <comando_composto>
    # FIRST(parte_decl_var) = { PALAVRA_RESERVADA_INT, PALAVRA_RESERVADA_BOOLEAN }
    # FIRST(parte_decl_sub_rotinas) = { PALAVRA_RESERVADA_PROCEDURE }
    # FIRST(comando_composto) = { PALAVRA_RESERVADA_BEGIN }
    'bloco': {
        'PALAVRA_RESERVADA_INT': ['parte_decl_var', 'parte_decl_sub_rotinas', 'comando_composto'],
        'PALAVRA_RESERVADA_BOOLEAN': ['parte_decl_var', 'parte_decl_sub_rotinas', 'comando_composto'],
        'PALAVRA_RESERVADA_PROCEDURE': ['parte_decl_sub_rotinas', 'comando_composto'],
        'PALAVRA_RESERVADA_BEGIN': ['parte_decl_var', 'parte_decl_sub_rotinas', 'comando_composto']
    },
    'comando_composto': {
        'PALAVRA_RESERVADA_BEGIN': ['PALAVRA_RESERVADA_BEGIN', 'lista_comandos', 'PALAVRA_RESERVADA_END']
    },
    'lista_comandos': {
        'IDENTIFICADOR': ['comando', 'lista_comandos_tail'],
        'PALAVRA_RESERVADA_IF': ['comando', 'lista_comandos_tail'],
        'PALAVRA_RESERVADA_WHILE': ['comando', 'lista_comandos_tail'],
        'PALAVRA_RESERVADA_BEGIN': ['comando', 'lista_comandos_tail'],
        'PALAVRA_RESERVADA_END': ['ε'],
    },
    'lista_comandos_tail': {
        'PONTO_E_VIRGULA': ['PONTO_E_VIRGULA', 'comando', 'lista_comandos_tail'],
        'PALAVRA_RESERVADA_END': ['ε']
    },
    'comando': {
        'IDENTIFICADOR': ['atribuicao'],
        'PALAVRA_RESERVADA_IF': ['comando_condicional1'],
        'PALAVRA_RESERVADA_WHILE': ['comando_repetitivo1'],
        'PALAVRA_RESERVADA_BEGIN': ['comando_composto'],
    },
    'atribuicao': {
        'IDENTIFICADOR': ['variavel', 'ATRIBUICAO', 'expressao']
    },
    
    #### Declarações ####
    # 3. <parte_decl_var> ::= decl_var parte_decl_var_tail
    'parte_decl_var': {
        'PALAVRA_RESERVADA_INT': ['decl_var', 'parte_decl_var_tail'],
        'PALAVRA_RESERVADA_BOOLEAN': ['decl_var', 'parte_decl_var_tail'],
        'PALAVRA_RESERVADA_PROCEDURE': ['ε'],
        'PALAVRA_RESERVADA_BEGIN': ['ε']
    },
    # 3b. <parte_decl_var_tail> ::= ; decl_var parte_decl_var_tail | ε
    'parte_decl_var_tail': {
        'PONTO_E_VIRGULA': ['PONTO_E_VIRGULA', 'decl_var', 'parte_decl_var_tail'],
        'PALAVRA_RESERVADA_PROCEDURE': ['ε'],
        'PALAVRA_RESERVADA_BEGIN': ['ε']
    },
    # 4. <decl_var> ::= tipo lista_id
    'decl_var': {
        'PALAVRA_RESERVADA_INT': ['tipo', 'lista_id'],
        'PALAVRA_RESERVADA_BOOLEAN': ['tipo', 'lista_id'],
        'PALAVRA_RESERVADA_PROCEDURE': ['ε'],
        'PALAVRA_RESERVADA_BEGIN': ['ε']
    },
    # 4b. <tipo> ::= int | boolean
    'tipo': {
        'PALAVRA_RESERVADA_INT': ['PALAVRA_RESERVADA_INT'],
        'PALAVRA_RESERVADA_BOOLEAN': ['PALAVRA_RESERVADA_BOOLEAN']
    },
    # 5. <lista_id> ::= IDENTIFICADOR lista_id_tail
    'lista_id': {
        'IDENTIFICADOR': ['IDENTIFICADOR', 'lista_id_tail']
    },
    # 5b. <lista_id_tail> ::= , IDENTIFICADOR lista_id_tail | ε
    'lista_id_tail': {
        'VIRGULA': ['VIRGULA', 'IDENTIFICADOR', 'lista_id_tail'],
        'SEPARADOR': ['ε'],
        'PONTO_E_VIRGULA': ['ε'],
        'PALAVRA_RESERVADA_PROCEDURE': ['ε'],
        'PALAVRA_RESERVADA_BEGIN': ['ε'],
        'FECHA_PARENTESES': ['ε'],
    },
    # 6. <parte_decl_sub_rotinas> ::= decl_sub_rotinas parte_decl_sub_rotinas_tail
    'parte_decl_sub_rotinas': {
        'PALAVRA_RESERVADA_PROCEDURE': ['decl_sub_rotinas', 'parte_decl_sub_rotinas_tail'],
        'PALAVRA_RESERVADA_BEGIN': ['ε']
    },
    # 6b. <parte_decl_sub_rotinas_tail> ::= ; decl_sub_rotinas parte_decl_sub_rotinas_tail | ε
    'parte_decl_sub_rotinas_tail': {
        'PONTO_E_VIRGULA': ['PONTO_E_VIRGULA', 'decl_sub_rotinas', 'parte_decl_sub_rotinas_tail'],
        'PALAVRA_RESERVADA_BEGIN': ['ε'],
    },
    # 7. <decl_sub_rotinas> ::= procedure IDENTIFICADOR param_formais_opt ; bloco
    'decl_sub_rotinas': {
        'PALAVRA_RESERVADA_PROCEDURE': [
            'PALAVRA_RESERVADA_PROCEDURE', 'IDENTIFICADOR', 'param_formais_opt', 'PONTO_E_VIRGULA', 'parte_decl_var', 'bloco'
        ]
    },
    # 8. <param_formais_opt> ::= ( secao_param_formais param_formais_tail ) | ε
    'param_formais_opt': {
        'ABRE_PARENTESES': ['ABRE_PARENTESES', 'secao_param_formais', 'param_formais_tail', 'FECHA_PARENTESES'],
        'PONTO_E_VIRGULA': ['ε'],
    },
    # 8b. <param_formais_tail> ::= ; secao_param_formais param_formais_tail | ε
    'param_formais_tail': {
        'PONTO_E_VIRGULA': ['PONTO_E_VIRGULA', 'secao_param_formais', 'param_formais_tail'],
        'FECHA_PARENTESES': ['ε'],
    },
    # 9. <secao_param_formais> ::= PALAVRA_RESERVADA_VAR lista_id SEPARADOR IDENTIFICADOR | lista_id SEPARADOR IDENTIFICADOR
    'secao_param_formais': {
        'PALAVRA_RESERVADA_VAR': ['PALAVRA_RESERVADA_VAR', 'lista_id', 'SEPARADOR', 'IDENTIFICADOR'],
        'IDENTIFICADOR': ['lista_id', 'SEPARADOR', 'IDENTIFICADOR'],
    },
    
    #### Expressoes ####
    
    # chamada_args_opt ::= (lista_expressao_opt) | ε
    'chamada_args_opt': {
        'ABRE_PARENTESES': ['ABRE_PARENTESES', 'lista_expressao_opt', 'FECHA_PARENTESES'],
        'PONTO_E_VIRGULA': ['ε'],
        'PALAVRA_RESERVADA_END': ['ε'],
        'PALAVRA_RESERVADA_ELSE': ['ε'],
    },
    # <lista_expressao_opt> ::= expressao lista_expressao_tail | ε
    'lista_expressao_opt': {
        'IDENTIFICADOR': ['expressao', 'lista_expressao_tail'],
        'NUMERO_INTEIRO': ['expressao', 'lista_expressao_tail'],
        'NUMERO_REAL': ['expressao', 'lista_expressao_tail'],
        'PALAVRA_RESERVADA_TRUE': ['expressao', 'lista_expressao_tail'],
        'PALAVRA_RESERVADA_FALSE': ['expressao', 'lista_expressao_tail'],
        'FECHA_PARENTESES': ['ε'],
    },
    # <lista_expressao_tail> ::= , expressao lista_expressao_tail | ε
    'lista_expressao_tail': {
        'VIRGULA': ['VIRGULA', 'expressao', 'lista_expressao_tail'],
        'FECHA_PARENTESES': ['ε'],
    },

    # 14. <comando_condicional1> ::= if expressao then comando [else comando]
    'comando_condicional1': {
        'PALAVRA_RESERVADA_IF': [
            'PALAVRA_RESERVADA_IF', 'ABRE_PARENTESES', 'expressao', 'FECHA_PARENTESES', 'PALAVRA_RESERVADA_THEN', 'comando', 'comando_condicional1_else'
        ]
    },
    'comando_condicional1_else': {
        'PALAVRA_RESERVADA_ELSE': ['PALAVRA_RESERVADA_ELSE', 'comando'],
        'PONTO_E_VIRGULA': ['ε'],
        'PALAVRA_RESERVADA_END': ['ε'],
    },

    # 15. <comando_repetitivo1> ::= while expressao do comando
    'comando_repetitivo1': {
        'PALAVRA_RESERVADA_WHILE': [
            'PALAVRA_RESERVADA_WHILE', 'expressao', 'PALAVRA_RESERVADA_DO', 'comando'
        ]
    },
    # 16. <expressao> ::= expressao_simples expressao_relacional_tail
    'expressao': {
        'IDENTIFICADOR': ['expressao_simples', 'expressao_relacional_tail'],
        'NUMERO_INTEIRO': ['expressao_simples', 'expressao_relacional_tail'],
        'NUMERO_REAL': ['expressao_simples', 'expressao_relacional_tail'],
        'PALAVRA_RESERVADA_TRUE': ['expressao_simples', 'expressao_relacional_tail'],
        'PALAVRA_RESERVADA_FALSE': ['expressao_simples', 'expressao_relacional_tail'],
        'ABRE_PARENTESES': ['expressao_simples', 'expressao_relacional_tail'],
        'OPERADOR_SOMA': ['expressao_simples', 'expressao_relacional_tail'],
        'OPERADOR_SUBTRACAO': ['expressao_simples', 'expressao_relacional_tail'],
        'PALAVRA_RESERVADA_NOT': ['expressao_simples', 'expressao_relacional_tail'],
    },
    # expressao_relacional_tail: caso tenha um relacional, segue, senão epsilon
    'expressao_relacional_tail': {
        'IGUALDADE': ['relacao', 'expressao_simples'],
        'DIFERENTE': ['relacao', 'expressao_simples'],
        'MENOR': ['relacao', 'expressao_simples'],
        'MENOR_IGUAL': ['relacao', 'expressao_simples'],
        'MAIOR_IGUAL': ['relacao', 'expressao_simples'],
        'MAIOR': ['relacao', 'expressao_simples'],
        # FOLLOW(expressao): fecha expressão
        'PONTO_E_VIRGULA': ['ε'],
        'FECHA_PARENTESES': ['ε'],
        'PALAVRA_RESERVADA_THEN': ['ε'],
        'PALAVRA_RESERVADA_DO': ['ε'],
        'PALAVRA_RESERVADA_END': ['ε'],
        'PALAVRA_RESERVADA_ELSE': ['ε'],
        'VIRGULA': ['ε'],
    },
    # 17. <relacao> ::= = | <> | < | <= | >= | >
    'relacao': {
        'IGUALDADE': ['IGUALDADE'],
        'DIFERENTE': ['DIFERENTE'],
        'MENOR': ['MENOR'],
        'MENOR_IGUAL': ['MENOR_IGUAL'],
        'MAIOR_IGUAL': ['MAIOR_IGUAL'],
        'MAIOR': ['MAIOR'],
    },

    # 18. <expressao_simples> ::= expressao_simples_inicio termo expressao_simples_tail
    'expressao_simples': {
        'OPERADOR_SOMA': ['expressao_simples_inicio', 'termo', 'expressao_simples_tail'],
        'OPERADOR_SUBTRACAO': ['expressao_simples_inicio', 'termo', 'expressao_simples_tail'],
        'IDENTIFICADOR': ['expressao_simples_inicio', 'termo', 'expressao_simples_tail'],
        'NUMERO_INTEIRO': ['expressao_simples_inicio', 'termo', 'expressao_simples_tail'],
        'NUMERO_REAL': ['expressao_simples_inicio', 'termo', 'expressao_simples_tail'],
        'PALAVRA_RESERVADA_TRUE': ['expressao_simples_inicio', 'termo', 'expressao_simples_tail'],
        'PALAVRA_RESERVADA_FALSE': ['expressao_simples_inicio', 'termo', 'expressao_simples_tail'],
        'ABRE_PARENTESES': ['expressao_simples_inicio', 'termo', 'expressao_simples_tail'],
        'PALAVRA_RESERVADA_NOT': ['expressao_simples_inicio', 'termo', 'expressao_simples_tail'],
    },
    'expressao_simples_inicio': {
        'OPERADOR_SOMA': ['OPERADOR_SOMA'],
        'OPERADOR_SUBTRACAO': ['OPERADOR_SUBTRACAO'],
        'IDENTIFICADOR': ['ε'],
        'NUMERO_INTEIRO': ['ε'],
        'NUMERO_REAL': ['ε'],
        'PALAVRA_RESERVADA_TRUE': ['ε'],
        'PALAVRA_RESERVADA_FALSE': ['ε'],
        'ABRE_PARENTESES': ['ε'],
        'PALAVRA_RESERVADA_NOT': ['ε'],
    },
    # <expressao_simples_tail> ::= (+ | - | or) termo expressao_simples_tail | ε
    'expressao_simples_tail': {
        'OPERADOR_SOMA': ['operador_soma_ou_sub_ou_or', 'termo', 'expressao_simples_tail'],
        'OPERADOR_SUBTRACAO': ['operador_soma_ou_sub_ou_or', 'termo', 'expressao_simples_tail'],
        'PALAVRA_RESERVADA_OR': ['operador_soma_ou_sub_ou_or', 'termo', 'expressao_simples_tail'],
        # FOLLOW(expressao_simples)
        'IGUALDADE': ['ε'],
        'DIFERENTE': ['ε'],
        'MENOR': ['ε'],
        'MENOR_IGUAL': ['ε'],
        'MAIOR_IGUAL': ['ε'],
        'MAIOR': ['ε'],
        'PONTO_E_VIRGULA': ['ε'],
        'FECHA_PARENTESES': ['ε'],
        'PALAVRA_RESERVADA_THEN': ['ε'],
        'PALAVRA_RESERVADA_DO': ['ε'],
        'PALAVRA_RESERVADA_END': ['ε'],
        'PALAVRA_RESERVADA_ELSE': ['ε'],
        'VIRGULA': ['ε'],
    },
    'operador_soma_ou_sub_ou_or': {
        'OPERADOR_SOMA': ['OPERADOR_SOMA'],
        'OPERADOR_SUBTRACAO': ['OPERADOR_SUBTRACAO'],
        'PALAVRA_RESERVADA_OR': ['PALAVRA_RESERVADA_OR'],
    },

    # 19. <termo> ::= fator termo_tail
    'termo': {
        'IDENTIFICADOR': ['fator', 'termo_tail'],
        'NUMERO_INTEIRO': ['fator', 'termo_tail'],
        'NUMERO_REAL': ['fator', 'termo_tail'],
        'PALAVRA_RESERVADA_TRUE': ['fator', 'termo_tail'],
        'PALAVRA_RESERVADA_FALSE': ['fator', 'termo_tail'],
        'ABRE_PARENTESES': ['fator', 'termo_tail'],
        'OPERADOR_SOMA': ['fator', 'termo_tail'],
        'OPERADOR_SUBTRACAO': ['fator', 'termo_tail'],
        'PALAVRA_RESERVADA_NOT': ['fator', 'termo_tail'],
    },
    # <termo_tail> ::= (* | div | and) fator termo_tail | ε
    'termo_tail': {
        'OPERADOR_MULTIPLICACAO': ['operador_mul_div_and', 'fator', 'termo_tail'],
        'OPERADOR_DIV': ['operador_mul_div_and', 'fator', 'termo_tail'],
        'PALAVRA_RESERVADA_AND': ['operador_mul_div_and', 'fator', 'termo_tail'],
        # FOLLOW(termo)
        'OPERADOR_SOMA': ['ε'],
        'OPERADOR_SUBTRACAO': ['ε'],
        'PALAVRA_RESERVADA_OR': ['ε'],
        'IGUALDADE': ['ε'],
        'DIFERENTE': ['ε'],
        'MENOR': ['ε'],
        'MENOR_IGUAL': ['ε'],
        'MAIOR_IGUAL': ['ε'],
        'MAIOR': ['ε'],
        'PONTO_E_VIRGULA': ['ε'],
        'FECHA_PARENTESES': ['ε'],
        'PALAVRA_RESERVADA_THEN': ['ε'],
        'PALAVRA_RESERVADA_DO': ['ε'],
        'PALAVRA_RESERVADA_END': ['ε'],
        'PALAVRA_RESERVADA_ELSE': ['ε'],
        'VIRGULA': ['ε'],
    },
    'operador_mul_div_and': {
        'OPERADOR_MULTIPLICACAO': ['OPERADOR_MULTIPLICACAO'],
        'OPERADOR_DIV': ['OPERADOR_DIV'],
        'PALAVRA_RESERVADA_AND': ['PALAVRA_RESERVADA_AND'],
    },

    # 20. <fator> ::= variavel | numero | (expressao) | not fator
    'fator': {
        'IDENTIFICADOR': ['variavel'],
        'NUMERO_INTEIRO': ['numero'],
        'NUMERO_REAL': ['numero'],
        'ABRE_PARENTESES': ['ABRE_PARENTESES', 'expressao', 'FECHA_PARENTESES'],
        'OPERADOR_SOMA': ['sinal', 'fator'],  # Suporta fator negativo/positivo
        'OPERADOR_SUBTRACAO': ['sinal', 'fator'],
        'PALAVRA_RESERVADA_NOT': ['PALAVRA_RESERVADA_NOT', 'fator'],
        'PALAVRA_RESERVADA_TRUE': ['PALAVRA_RESERVADA_TRUE'],
        'PALAVRA_RESERVADA_FALSE': ['PALAVRA_RESERVADA_FALSE'],
    },
    'sinal': {
        'OPERADOR_SOMA': ['OPERADOR_SOMA'],
        'OPERADOR_SUBTRACAO': ['OPERADOR_SUBTRACAO'],
    },

    # 21. <variavel> ::= IDENTIFICADOR variavel_sufixo
    'variavel': {
        'IDENTIFICADOR': ['IDENTIFICADOR', 'variavel_sufixo']
    },
    'variavel_sufixo': {
        'ABRE_COLCHETES': ['ABRE_COLCHETES', 'expressao', 'FECHA_COLCHETES'],
        # FOLLOW(variavel)
        'ATRIBUICAO': ['ε'],
        'OPERADOR_SOMA': ['ε'],
        'OPERADOR_SUBTRACAO': ['ε'],
        'OPERADOR_MULTIPLICACAO': ['ε'],
        'OPERADOR_DIV': ['ε'],
        'PALAVRA_RESERVADA_AND': ['ε'],
        'PALAVRA_RESERVADA_OR': ['ε'],
        'IGUALDADE': ['ε'],
        'DIFERENTE': ['ε'],
        'MENOR': ['ε'],
        'MENOR_IGUAL': ['ε'],
        'MAIOR_IGUAL': ['ε'],
        'MAIOR': ['ε'],
        'VIRGULA': ['ε'],
        'FECHA_PARENTESES': ['ε'],
        'PONTO_E_VIRGULA': ['ε'],
        'PALAVRA_RESERVADA_THEN': ['ε'],
        'PALAVRA_RESERVADA_DO': ['ε'],
        'PALAVRA_RESERVADA_END': ['ε'],
        'PALAVRA_RESERVADA_ELSE': ['ε'],
        'PONTO': ['ε'],
    },

    # 22. <lista_de_expressoes> ::= expressao lista_de_expressoes_tail
    'lista_de_expressoes': {
        'IDENTIFICADOR': ['expressao', 'lista_de_expressoes_tail'],
        'NUMERO_INTEIRO': ['expressao', 'lista_de_expressoes_tail'],
        'NUMERO_REAL': ['expressao', 'lista_de_expressoes_tail'],
        'PALAVRA_RESERVADA_TRUE': ['expressao', 'lista_de_expressoes_tail'],
        'PALAVRA_RESERVADA_FALSE': ['expressao', 'lista_de_expressoes_tail'],
        'ABRE_PARENTESES': ['expressao', 'lista_de_expressoes_tail'],
        'OPERADOR_SOMA': ['expressao', 'lista_de_expressoes_tail'],
        'OPERADOR_SUBTRACAO': ['expressao', 'lista_de_expressoes_tail'],
        'PALAVRA_RESERVADA_NOT': ['expressao', 'lista_de_expressoes_tail'],
    },
    'lista_de_expressoes_tail': {
        'VIRGULA': ['VIRGULA', 'expressao', 'lista_de_expressoes_tail'],
        'FECHA_PARENTESES': ['ε'],
        'PONTO_E_VIRGULA': ['ε'],
    },

    # <numero> ::= NUMERO_INTEIRO | NUMERO_REAL
    'numero': {
        'NUMERO_INTEIRO': ['NUMERO_INTEIRO'],
        'NUMERO_REAL': ['NUMERO_REAL'],
    }
}

def analisar_declaracoes(tokens):
    pilha = ['$', 'programa']
    pos = 0
    tamanho = len(tokens)
    
    print(tokens)

    sync_tokens = {}

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
        
        print(f"Pilha: {pilha} | Topo: {topo} | Token atual: {atual}")

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
                if 'ε' in tabela_sintatica[topo].values():
                    continue  # ← AGORA aceita epsilon se não há produção para o lookahead
                else:
                    erros.append(f"Erro sintático: token inesperado '{lexema_atual()}' na linha {linha_atual()}. Tentando recuperação...")

                    sync_set = sync_tokens.get(topo, ['$'])
                    while atual not in sync_set and atual != '$':
                        pos += 1
                        atual = token_atual()
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

from lark import Lark

def analisar_pascal_lark(codigo_fonte, caminho_gramatica="grammar.lark"):
    # Lê a gramática do arquivo
    with open(caminho_gramatica, "r", encoding="utf-8") as f:
        gramatica = f.read()

    # Cria o parser do Lark
    parser = Lark(gramatica, start="start", parser="lalr")
    # Faz o parse do código-fonte
    arvore = parser.parse(codigo_fonte)
    
    return arvore
