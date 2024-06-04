# 2.0
from extract_grammar import GrammaticalQuadrupleExtraction


def finite_state_automata2(grammar_str):
    terminators, non_terminators, productions, start = GrammaticalQuadrupleExtraction().extract_grammar_components(
        grammar_str)
    states = terminators + ['My_end']  # 状态集合 K
    alphabet = non_terminators  # 符号集合 Σ
    transition_function = {}  # 转移函数 M
    start_state = ['My_end']  # 起始状态 S
    accept_state = [start]  # 接受状态 F

    matrix = {row_label: {col_label: None for col_label in alphabet} for row_label in states}
    for key in productions:
        for item in productions[key]:
            if len(item) == 1:  # 右部只有一个终结符
                if ('My_end', item[0]) not in transition_function:
                    transition_function[('My_end', item[0])] = [key]
                else:
                    transition_function[('My_end', item[0])].append(key)
                # matrix['My_end'][item[0]] = key
            if len(item) == 2:
                if (item[0], item[1]) not in transition_function:
                    transition_function[(item[0], item[1])] = [key]
                else:
                    transition_function[(item[0], item[1])].append(key)
    return states, alphabet, transition_function, start_state, accept_state


def transition_function_print(transition_function):
    result = ''
    for row_label, row_data in transition_function.items():
        # print("M",row_label, "=", row_data)
        result += "M(" + ','.join(row_label) + ") = {" + ','.join(row_data) + '}\n'
    return result


grammar_str8 = ("Z ::= Z a | A a | B b\n"
                "A ::= B a | Z a | a\n"
                "B ::= A b | B a | b")

grammar_str7 = ("A ::= B a | C b | c\n"
                "B ::= d a | A e | f\n"
                "C ::= B g | h")
if __name__ == '__main__':
    # finite_state_automata2(grammar_str8)
    states, alphabet, transition_function, start_state, accept_state = finite_state_automata2(grammar_str8)
    print(states)
    print(alphabet)
    print(transition_function)
    print(start_state)
    print(accept_state)
    # print()

    states = ['Z', 'A', 'B', 'My_end']
    alphabet = ['a', 'b']
    transition_function = {('Z', 'a'): ['Z', 'A'],
                           ('A', 'a'): ['Z'], ('B', 'b'): ['Z'],
                           ('B', 'a'): ['A', 'B'],('My_end', 'a'): ['A'],
                           ('A', 'b'): ['B'], ('My_end', 'b'): ['B']}
    start_state = ['My_end']
    accept_state = ['Z']