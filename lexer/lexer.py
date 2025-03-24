import re

class Lexer:
    """Classe responsável pela análise léxica."""

    PALAVRAS_RESERVADAS = {
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

    REGEX_TOKENS = [
        (r'\b(program|begin|end|if|then|else|while|do|procedure|var|int|boolean|true|false|read|write)\b', "PALAVRA_RESERVADA"),
        (r'[a-zA-Z_][a-zA-Z0-9_]*', "IDENTIFICADOR"),
        (r'\d+(\.\d+)?', "NUMERO"),
        (r'\s+', None)
    ]

    def __init__(self):
        self.regex_compiladas = [(re.compile(padrao), tipo) for padrao, tipo in self.REGEX_TOKENS]

    def analisar(self, expressao):
        """Realiza a análise léxica."""
        tokens_encontrados = []
        posicao = 0
        tamanho = len(expressao)

        while posicao < tamanho:
            match = None
            for regex, tipo in self.regex_compiladas:
                match = regex.match(expressao, posicao)
                if match:
                    if tipo:
                        lexema = match.group(0)
                        token_tipo = self.PALAVRAS_RESERVADAS.get(lexema, tipo)
                        tokens_encontrados.append((lexema, token_tipo))
                    break

            if not match:
                tokens_encontrados.append((expressao[posicao], "DESCONHECIDO"))
                posicao += 1
            else:
                posicao = match.end()

        return tokens_encontrados
