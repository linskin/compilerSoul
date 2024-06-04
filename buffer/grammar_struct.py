class GrammarStruct:
    def __init__(self, productions):
        self.productions = productions

    def add_production(self, non_terminal, production):
        if non_terminal in self.productions:
            self.productions[non_terminal].append(production)
        else:
            self.productions[non_terminal] = [production]

    def remove_production(self, non_terminal, production):
        if non_terminal in self.productions and production in self.productions[non_terminal]:
            self.productions[non_terminal].remove(production)
            if not self.productions[non_terminal]:  # If the set becomes empty, remove the key
                del self.productions[non_terminal]


if __name__ == '__main__':
    product = {'E': [['E', '+', 'T'], ['T']], 'T': [['T', '*', 'F'], ['F']], 'F': [['(', 'E', ')'], ['i']]}
    grammar = GrammarStruct(product)

    # Add a new production
    grammar.add_production('E', ['E', '-', 'T'])
    print("After adding production:", grammar.productions)

    # Remove an existing production
    grammar.remove_production('F', ['F'])
    print("After removing production:", grammar.productions)
