class Symbol:
    def __init__(self, name, type_, category, parameters=None):
        self.name = name
        self.type = type_        # Ex: 'int', 'boolean', None (para procedimentos)
        self.category = category # Ex: 'variável', 'procedimento'
        self.parameters = parameters or []  # Lista de (nome, tipo) se for procedimento

    def __repr__(self):
        return f"<Symbol {self.name} : {self.type} ({self.category})>"


class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Escopo global no início

    def enter_scope(self):
        """Cria um novo escopo (ex: início de um procedimento)"""
        self.scopes.append({})

    def exit_scope(self):
        """Sai do escopo atual"""
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise Exception("Tentativa de sair do escopo global.")

    def declare(self, name, type_, category, parameters=None):
        """Declara um novo símbolo no escopo atual"""
        scope = self.scopes[-1]
        if name in scope:
            raise Exception(f"Erro: símbolo '{name}' já declarado neste escopo.")
        scope[name] = Symbol(name, type_, category, parameters)

    def lookup(self, name):
        """Busca um símbolo nos escopos (de dentro para fora)"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Erro: símbolo '{name}' não foi declarado.")

    def current_scope(self):
        """Retorna os símbolos do escopo atual"""
        return self.scopes[-1]

    def __repr__(self):
        output = "TABELA DE SÍMBOLOS:\n"
        for i, scope in enumerate(self.scopes):
            output += f" Escopo {i}:\n"
            for name, symbol in scope.items():
                output += f"  - {name}: {symbol}\n"
        return output
