import copy

from five_part_extract import *


def transition_function_deterministic(states, alphabet, transition_function, start_state, accept_state):
    tf = copy.deepcopy(transition_function)
    mid_accept_state = copy.deepcopy(accept_state)
    new_tf = {}  # 创建一个新的字典来保存修改后的键值对

    tag = True
    while tag:
        # tag = False
        for key in tf:
            if len(tf[key]) != 1:
                # tag = True
                mid_key = "".join(tf[key])  # 将值拼接成一个字符串作为新键
                mid_key_list = tf[key]  # 将值列表作为新键的值
                new_values = {}
                for item in alphabet:
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
                # print(mid_key_judgment)
                for word in alphabet:
                    if (mid_key_judgment, word) in tf:
                        # print(mid_key_judgment)
                        tag = False
        if not tag:
            for key in tf:
                if len(tf[key]) != 1:
                    mid_list = ''.join(set(''.join(tf[key])))
                    tf[key] = [mid_list]
            # 如果新键含有终止状态，将其放入终止状态表
            for key in tf:
                for item in tf[key]:
                    # print(item)
                    for item_s in item:
                        if item_s in accept_state:
                            mid_accept_state.append(item)

    mid_accept_state = list(set(mid_accept_state))
    mid_state = list(set(states + mid_accept_state))
    return mid_state, alphabet, tf, start_state, mid_accept_state


if __name__ == '__main__':
    states, alphabet, transition_function, start_state, accept_state = finite_state_automata2(grammar_str8)
    mid_state, alphabet, tf, mid_start_state, mid_accept_state = (
        transition_function_deterministic(states, alphabet, transition_function, start_state, accept_state))

    # 输出更新后的字典
    print(mid_state)
    print(alphabet)
    print(transition_function_print(tf))
    print(mid_start_state)
    print(mid_accept_state)
    # print(tf)
