# Tabela sintática LL(1) para a linguagem LALG
# dicionário em Python, onde a chave é o símbolo não terminal e o valor é outro dicionário

tabela_sintatica = {
    'programa': {
        'PALAVRA_RESERVADA_PROGRAM': ['PALAVRA_RESERVADA_PROGRAM', 'IDENTIFICADOR', 'PONTO_E_VIRGULA', 'bloco', 'PONTO']
    },
    'bloco': {
        'PALAVRA_RESERVADA_INT': ['decl_var_e_subrotinas', 'comando_composto'],
        'PALAVRA_RESERVADA_BOOLEAN': ['decl_var_e_subrotinas', 'comando_composto'],
        'PALAVRA_RESERVADA_PROCEDURE': ['decl_var_e_subrotinas', 'comando_composto'],
        'PALAVRA_RESERVADA_BEGIN': ['decl_var_e_subrotinas', 'comando_composto']
    },
    'decl_var_e_subrotinas': {
        'PALAVRA_RESERVADA_INT': ['decl_var', 'decl_subrotinas'],
        'PALAVRA_RESERVADA_BOOLEAN': ['decl_var', 'decl_subrotinas'],
        'PALAVRA_RESERVADA_PROCEDURE': ['decl_subrotinas'],
        'PALAVRA_RESERVADA_BEGIN': ['ε']
    },
    'decl_var': {
        'PALAVRA_RESERVADA_INT': ['tipo', 'lista_identificadores', 'PONTO_E_VIRGULA', 'decl_var'],
        'PALAVRA_RESERVADA_BOOLEAN': ['tipo', 'lista_identificadores', 'PONTO_E_VIRGULA', 'decl_var'],
        'PALAVRA_RESERVADA_PROCEDURE': ['ε'],
        'PALAVRA_RESERVADA_BEGIN': ['ε']
    },
    'decl_subrotinas': {
        'PALAVRA_RESERVADA_PROCEDURE': ['decl_procedimento', 'decl_subrotinas'],
        'PALAVRA_RESERVADA_BEGIN': ['ε']
    },
    'decl_procedimento': {
        'PALAVRA_RESERVADA_PROCEDURE': ['PALAVRA_RESERVADA_PROCEDURE', 'IDENTIFICADOR', 'parametros_formais_opt', 'PONTO_E_VIRGULA', 'bloco', 'PONTO_E_VIRGULA']
    },
    'parametros_formais_opt': {
        'ABRE_PARENTESES': ['parametros_formais'],
        'PONTO_E_VIRGULA': ['ε'],
        'PALAVRA_RESERVADA_BEGIN': ['ε']
    },
    'parametros_formais': {
        'ABRE_PARENTESES': ['ABRE_PARENTESES', 'secao_parametros', 'secao_parametros_tail', 'FECHA_PARENTESES']
    },
    'secao_parametros_tail': {
        'PONTO_E_VIRGULA': ['PONTO_E_VIRGULA', 'secao_parametros', 'secao_parametros_tail'],
        'FECHA_PARENTESES': ['ε']
    },
    'secao_parametros': {
        'PALAVRA_RESERVADA_VAR': ['PALAVRA_RESERVADA_VAR', 'lista_identificadores', 'SEPARADOR', 'tipo'],
        'IDENTIFICADOR': ['lista_identificadores', 'SEPARADOR', 'tipo']
    },
    'tipo': {
        'PALAVRA_RESERVADA_INT': ['PALAVRA_RESERVADA_INT'],
        'PALAVRA_RESERVADA_BOOLEAN': ['PALAVRA_RESERVADA_BOOLEAN']
    },
    'lista_identificadores': {
        'IDENTIFICADOR': ['IDENTIFICADOR', 'lista_identificadores_tail']
    },
    'lista_identificadores_tail': {
        'VIRGULA': ['VIRGULA', 'IDENTIFICADOR', 'lista_identificadores_tail'],
        'SEPARADOR': ['ε'],
        'PONTO_E_VIRGULA': ['ε']
    },
    'comando_composto': {
        'PALAVRA_RESERVADA_BEGIN': ['PALAVRA_RESERVADA_BEGIN', 'comando', 'lista_comandos_tail', 'PALAVRA_RESERVADA_END']
    },
    'lista_comandos_tail': {
        'PONTO_E_VIRGULA': ['PONTO_E_VIRGULA', 'comando', 'lista_comandos_tail'],
        'PALAVRA_RESERVADA_END': ['ε']
    },
    'comando': {
        'IDENTIFICADOR': ['atribuicao_ou_chamada'],
        'PALAVRA_RESERVADA_BEGIN': ['comando_composto'],
        'PALAVRA_RESERVADA_IF': ['comando_condicional'],
        'PALAVRA_RESERVADA_WHILE': ['comando_repetitivo'],
        'PALAVRA_RESERVADA_END': ['ε']  # <-- Permite bloco vazio
    },
    'atribuicao_ou_chamada': {
        'IDENTIFICADOR': ['IDENTIFICADOR', 'atribuicao_ou_chamada_tail']
    },
    'atribuicao_ou_chamada_tail': {
        'ATRIBUICAO': ['ATRIBUICAO', 'expressao'],
        'ABRE_PARENTESES': ['ABRE_PARENTESES', 'lista_de_expressões', 'FECHA_PARENTESES'],
        'PONTO_E_VIRGULA': ['ε']
    },
    'lista_de_expressões': {
        'IDENTIFICADOR': ['expressao', 'lista_de_expressões_tail'],
        'NUMERO_INTEIRO': ['expressao', 'lista_de_expressões_tail']
    },
    'lista_de_expressões_tail': {
        'VIRGULA': ['VIRGULA', 'expressao', 'lista_de_expressões_tail'],
        'FECHA_PARENTESES': ['ε']
    },
    'comando_repetitivo': {
        'PALAVRA_RESERVADA_WHILE': ['PALAVRA_RESERVADA_WHILE', 'expressao', 'PALAVRA_RESERVADA_DO', 'comando']
    },
    'comando_condicional': {
        'PALAVRA_RESERVADA_IF': [
            'PALAVRA_RESERVADA_IF',
            'ABRE_PARENTESES',
            'expressao',
            'FECHA_PARENTESES',
            'PALAVRA_RESERVADA_THEN',
            'comando',
            'comando_condicional_else'
        ]
    },
    'comando_condicional_else': {
        'PALAVRA_RESERVADA_ELSE': ['PALAVRA_RESERVADA_ELSE', 'comando'],
        'PONTO_E_VIRGULA': ['ε'],
        'PALAVRA_RESERVADA_END': ['ε']
    },
    'expressao': {
        'IDENTIFICADOR':            ['expressao_simples', 'expressao_relacional_tail'],
        'NUMERO_INTEIRO':           ['expressao_simples', 'expressao_relacional_tail'],
        'ABRE_PARENTESES':          ['expressao_simples', 'expressao_relacional_tail'],
        'OPERADOR_SUBTRACAO':       ['expressao_simples', 'expressao_relacional_tail'],
        'OPERADOR_SOMA':            ['expressao_simples', 'expressao_relacional_tail'],
        'PALAVRA_RESERVADA_TRUE':   ['expressao_simples', 'expressao_relacional_tail'],
        'PALAVRA_RESERVADA_FALSE':  ['expressao_simples', 'expressao_relacional_tail']
    },
    'expressao_relacional_tail': {
        'MENOR': ['operador_relacional', 'expressao_simples'],
        'MAIOR': ['operador_relacional', 'expressao_simples'],
        'MENOR_IGUAL': ['operador_relacional', 'expressao_simples'],
        'MAIOR_IGUAL': ['operador_relacional', 'expressao_simples'],
        'IGUALDADE': ['operador_relacional', 'expressao_simples'],
        'DIFERENTE': ['operador_relacional', 'expressao_simples'],
        'FECHA_PARENTESES': ['ε'],
        'PALAVRA_RESERVADA_THEN': ['ε'],
        'PONTO_E_VIRGULA': ['ε']
    },
    'operador_relacional': {
        'MENOR': ['MENOR'],
        'MAIOR': ['MAIOR'],
        'MENOR_IGUAL': ['MENOR_IGUAL'],
        'MAIOR_IGUAL': ['MAIOR_IGUAL'],
        'IGUALDADE': ['IGUALDADE'],
        'DIFERENTE': ['DIFERENTE']
    },
    'expressao_simples': {
        'IDENTIFICADOR':            ['termo', 'expressao_simples_tail'],
        'NUMERO_INTEIRO':           ['termo', 'expressao_simples_tail'],
        'ABRE_PARENTESES':          ['termo', 'expressao_simples_tail'],
        'OPERADOR_SUBTRACAO':       ['OPERADOR_SUBTRACAO', 'termo', 'expressao_simples_tail'],
        'OPERADOR_SOMA':            ['OPERADOR_SOMA', 'termo', 'expressao_simples_tail'],
        'PALAVRA_RESERVADA_TRUE':   ['termo', 'expressao_simples_tail'],
        'PALAVRA_RESERVADA_FALSE':  ['termo', 'expressao_simples_tail']
    },
    'expressao_simples_tail': {
        'OPERADOR_SOMA':            ['OPERADOR_SOMA', 'termo', 'expressao_simples_tail'],
        'OPERADOR_SUBTRACAO':       ['OPERADOR_SUBTRACAO', 'termo', 'expressao_simples_tail'],
        'PALAVRA_RESERVADA_OR':     ['PALAVRA_RESERVADA_OR', 'termo', 'expressao_simples_tail'],
        # itens de FOLLOW para ε
        'PALAVRA_RESERVADA_THEN':   ['ε'],
        'PALAVRA_RESERVADA_DO':     ['ε'],
        'PONTO_E_VIRGULA':          ['ε'],
        'PALAVRA_RESERVADA_END':    ['ε'],
        'IGUALDADE':                ['ε'],
        'DIFERENTE':                ['ε'],
        'MAIOR':                    ['ε'],
        'MENOR':                    ['ε'],
        'MAIOR_IGUAL':              ['ε'],
        'MENOR_IGUAL':              ['ε']
    },
    'termo': {
        'IDENTIFICADOR':            ['fator', 'termo_tail'],
        'NUMERO_INTEIRO':           ['fator', 'termo_tail'],
        'ABRE_PARENTESES':          ['fator', 'termo_tail'],
        'OPERADOR_SUBTRACAO':       ['fator', 'termo_tail'],  # unário já consumido em expresao_simples
        'PALAVRA_RESERVADA_TRUE':   ['fator', 'termo_tail'],
        'PALAVRA_RESERVADA_FALSE':  ['fator', 'termo_tail']
    },
    'termo_tail': {
        'OPERADOR_MULTIPLICACAO':   ['OPERADOR_MULTIPLICACAO', 'fator', 'termo_tail'],
        'OPERADOR_DIV':             ['OPERADOR_DIV', 'fator', 'termo_tail'],
        'PALAVRA_RESERVADA_AND':    ['PALAVRA_RESERVADA_AND', 'fator', 'termo_tail'],
        # itens de FOLLOW para ε
        'PALAVRA_RESERVADA_OR':     ['ε'],
        'OPERADOR_SOMA':            ['ε'],
        'OPERADOR_SUBTRACAO':       ['ε'],
        'PALAVRA_RESERVADA_THEN':   ['ε'],
        'PALAVRA_RESERVADA_DO':     ['ε'],
        'PALAVRA_RESERVADA_END':    ['ε'],
        'PONTO_E_VIRGULA':          ['ε'],
        'FECHA_PARENTESES':         ['ε']
    },
    'fator': {
        'IDENTIFICADOR':            ['IDENTIFICADOR'],
        'NUMERO_INTEIRO':           ['NUMERO_INTEIRO'],
        'ABRE_PARENTESES':          ['ABRE_PARENTESES', 'expressao', 'FECHA_PARENTESES'],
        'OPERADOR_SUBTRACAO':       ['OPERADOR_SUBTRACAO', 'fator'],
        'OPERADOR_SOMA':            ['OPERADOR_SOMA',      'fator'],
        'PALAVRA_RESERVADA_TRUE':   ['PALAVRA_RESERVADA_TRUE'],
        'PALAVRA_RESERVADA_FALSE':  ['PALAVRA_RESERVADA_FALSE']
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
                if any(producao == ['ε'] for producao in tabela_sintatica[topo].values()):
                    continue
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
