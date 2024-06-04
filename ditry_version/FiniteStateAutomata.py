from derivation_visualizer.extract_grammar import GrammaticalQuadrupleExtraction


class FiniteStateAutomata:
    def __init__(self, grammar_str):
        self.grammar_str = grammar_str
        self.states = []
        self.alphabet = []
        self.transition_function = {}
        self.start_state = []
        self.accept_state = []

    def extract_components(self):
        terminators, non_terminators, productions, start = GrammaticalQuadrupleExtraction().extract_grammar_components(
            self.grammar_str)
        self.states = terminators + ['My_end']  # 状态集合 K
        self.alphabet = non_terminators  # 符号集合 Σ
        self.start_state = ['My_end']  # 起始状态 S
        self.accept_state = [start]  # 接受状态 F

        matrix = {row_label: {col_label: None for col_label in self.alphabet} for row_label in self.states}
        for key in productions:
            for item in productions[key]:
                if len(item) == 1:  # 右部只有一个终结符
                    if ('My_end', item[0]) not in self.transition_function:
                        self.transition_function[('My_end', item[0])] = [key]
                    else:
                        self.transition_function[('My_end', item[0])].append(key)
                if len(item) == 2:
                    if (item[0], item[1]) not in self.transition_function:
                        self.transition_function[(item[0], item[1])] = [key]
                    else:
                        self.transition_function[(item[0], item[1])].append(key)
        return self.states, self.alphabet, self.transition_function, self.start_state, self.accept_state

    def print_transition_function(self):
        result = ''
        for row_label, row_data in self.transition_function.items():
            result += "M(" + ','.join(row_label) + ") = {" + ','.join(row_data) + '}\n'
        return result

    def print_components(self):
        print("K : {" + ','.join(self.states) + '}\n')
        print("Σ : {" + ','.join(self.alphabet) + '}\n')
        print("M : \n")
        print(self.print_transition_function())
        print("S : {" + ','.join(self.start_state) + '}\n')
        print("F : {" + ','.join(self.accept_state) + '}')


if __name__ == '__main__':
    # Example usage:
    grammar_str8 = ("Z ::= Z a | A a | B b\n"
                    "A ::= B a | Z a | a\n"
                    "B ::= A b | B a | b")

    fsa = FiniteStateAutomata(grammar_str8)
    print(fsa.extract_components())

    # fsa.print_components()
