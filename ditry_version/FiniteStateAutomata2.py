import copy
from derivation_visualizer.extract_grammar import GrammaticalQuadrupleExtraction
from FiniteAutomaton import construct_fsm


class FiniteStateAutomata2:
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

    def construct_fsm(self):
        tf = copy.deepcopy(self.transition_function)
        mid_accept_state = copy.deepcopy(self.accept_state)
        new_tf = {}  # 创建一个新的字典来保存修改后的键值对

        tag = True
        while tag:
            for key in tf:
                if len(tf[key]) != 1:
                    mid_key = "".join(tf[key])  # 将值拼接成一个字符串作为新键
                    mid_key_list = tf[key]  # 将值列表作为新键的值
                    for item in self.alphabet:
                        list1 = []
                        for sub_key in mid_key_list:
                            try:
                                list1 += tf[(sub_key, item)]
                            except KeyError:
                                continue
                        unique_list = list(set(list1))
                        new_tf[(mid_key, item)] = unique_list  # 将新键值对添加到新字典中
                    tf[key] = [mid_key]
            # 更新原始字典
            tf.update(new_tf)
            # 检测是否到达转化完成的条件
            for key in tf:
                if len(tf[key]) != 1:
                    mid_key_judgment = ''.join(tf[key])
                    for word in self.alphabet:
                        if (mid_key_judgment, word) in tf:
                            tag = False
            if not tag:
                for key in tf:
                    if len(tf[key]) != 1:
                        mid_list = ''.join(set(''.join(tf[key])))
                        tf[key] = [mid_list]
                # 如果新键含有终止状态，将其放入终止状态表
                for key in tf:
                    for item in tf[key]:
                        for item_s in item:
                            if item_s in self.accept_state:
                                mid_accept_state.append(item)
                mid_accept_state = list(set(mid_accept_state))
                mid_state = list(set(self.states + mid_accept_state))
                return mid_state, tf, mid_accept_state


if __name__ == '__main__':
    # Example usage:
    grammar_str8 = ("Z ::= Z a | A a | B b\n"
                    "A ::= B a | Z a | a\n"
                    "B ::= A b | B a | b")

    fsa = FiniteStateAutomata2(grammar_str8)
    states, alphabet, transition_function, start_state, accept_state = fsa.extract_components()
    mid_state, new_tf, mid_accept_state = fsa.construct_fsm()

    print("Mid States: ", mid_state)
    print("Updated Transition Function: ")
    print(fsa.print_transition_function())
    print("Mid Accept State: ", mid_accept_state)

    fsm = construct_fsm(mid_state, alphabet, transition_function, start_state, mid_accept_state)

    # 测试字符串
    test_strings = ['ba', 'babb', 'babba', 'babbbb', 'bb']

    # 运行有穷状态自动机并输出结果
    for s in test_strings:
        print(f"String '{s}' matches: {fsm.run(s)}")
