from FiniteStateAutomata import FiniteStateAutomata


class FiniteAutomaton:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

    def run(self, string):
        current_state = self.start_state
        for symbol in string:
            if (current_state, symbol) in self.transition_function:
                current_state = self.transition_function[(current_state, symbol)]
            else:
                return False
        return current_state in self.accept_states



# 从给定的五元组构建有穷状态自动机
def construct_fsm(K, sigma, M, S, F):
    return FiniteAutomaton(K, sigma, M, S, F)


if __name__ == '__main__':
    grammar_str = ("B ::= A 1 | B 0 | B 1 | 1\n"
                   "A ::= A 0 | 0\n")
    fsa = FiniteStateAutomata(grammar_str)
    fsa.extract_components()
    K, sigma, M, S, F = fsa.print_components()

    # 构建有穷状态自动机
    fsm = construct_fsm(K, sigma, M, S, F)

    # 测试字符串
    test_strings = ['010', '111', '1001', '00', '11']

    # 运行有穷状态自动机并输出结果
    for s in test_strings:
        print(f"String '{s}' matches: {fsm.run(s)}")