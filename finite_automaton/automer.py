from finite_automaton.compresses import automata_minimization
from finite_automaton.five_part_extract import finite_state_automata2, grammar_str8, transition_function_print
from finite_automaton.deterministic import transition_function_deterministic


class FiniteAutomaton:
    def __init__(self, K, sigma, M, S, F):
        self.states = set(K)  # 状态集合
        self.alphabet = set(sigma)  # 输入字母表
        self.transitions = M  # 状态转移函数
        self.start_state = S[0]  # 初始状态
        self.accept_states = F  # 接受状态集合

    def run(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if (current_state, symbol) in self.transitions:
                mid_state = self.transitions[(current_state, symbol)]
                current_state = mid_state[0]
                # print(current_state)
            else:
                return False
        return current_state in self.accept_states


# 从给定的五元组构建有穷状态自动机
def construct_fsm(K, sigma, M, S, F):
    return FiniteAutomaton(K, sigma, M, S, F)


if __name__ == '__main__':
    states, alphabet, transition_function, start_state, accept_state = finite_state_automata2(grammar_str8)
    mid_state, alphabet, tf, mid_start_state, mid_accept_state = (
        transition_function_deterministic(states, alphabet, transition_function, start_state, accept_state))
    states, alphabet, mid_transition_function, start_state, accept_state = automata_minimization(mid_state, alphabet,
                                                                                                 tf,
                                                                                                 mid_start_state,
                                                                                                 mid_accept_state)
    # 构建有穷状态自动机
    fsm = construct_fsm(states, alphabet, mid_transition_function, start_state, accept_state)

    # 测试字符串
    test_strings = ['ba', 'babb', 'babbabb', 'aaaa', 'baa', 'babaa']

    html_output = "<html><head><title>Finite State Automaton Output</title></head><body>"
    html_output += "<h2>Finite State Automaton Output</h2>"
    html_output += "<h3>States: {" + ', '.join(states) + '}</h3>'
    html_output += "<h3>Alphabet: {" + ', '.join(alphabet) + '}</h3>'
    html_output += "<h3>Transition Function:</h3>"
    html_output += "<pre>" + transition_function_print(mid_transition_function) + "</pre>"
    html_output += "<h3>Start State: {" + ', '.join(start_state) + '}</h3>'
    html_output += "<h3>Accept State: {" + ', '.join(accept_state) + '}</h3>'
    html_output += "<h3>Test Strings and Results:</h3>"
    html_output += "<ul>"
    for s in test_strings:
        html_output += "<li>String '" + s + "' matches: " + str(fsm.run(s)) + "</li>"
    html_output += "</ul>"
    html_output += "</body></html>"

    with open("fsm_output.html", "w") as f:
        f.write(html_output)

    print("Output saved to fsm_output.html")
    import webbrowser

    # Open the HTML file in the default web browser
    webbrowser.open("fsm_output.html")
