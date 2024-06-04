import copy

from finite_automaton.five_part_extract import finite_state_automata2, grammar_str8, transition_function_print
from finite_automaton.deterministic import transition_function_deterministic


def minimize_dfa(mid_state, alphabet, tf, final_states):
    transition_function = copy.deepcopy(tf)
    # 初始划分，将终态和非终态分开
    partition = [set(final_states), set(mid_state) - set(final_states)]
    # print(partition)

    while True:
        new_partition = []
        for group in partition:
            split_group = []
            for state in group:
                transitions = {}
                for symbol in alphabet:
                    try:
                        next_state = transition_function[(state, symbol)][0]
                    except KeyError:
                        continue
                    # 查找状态的转移目标所在的分组
                    for idx, part in enumerate(partition):
                        if next_state in part:
                            transitions[symbol] = idx
                            break
                split_group.append((state, transitions))

            # 根据转移目标所在的分组将状态分组
            groups = {}
            for state, trans in split_group:
                key = tuple(trans.values())
                if key not in groups:
                    groups[key] = [state]
                else:
                    groups[key].append(state)
            print(groups)
            # 将分组结果加入到新分组列表中
            new_partition.extend(groups.values())

        # 如果新分组和旧组相同，则达到最小化
        if new_partition == partition:
            break
        else:
            partition = new_partition

    # 将等价状态替换为代表状态
    equivalent_states = {}
    for idx, group in enumerate(partition):
        for state in group:
            equivalent_states[state] = idx

    return equivalent_states


def automata_minimization(states, alphabet, transition_function, start_state, accept_state):
    eqs = minimize_dfa(states, alphabet, transition_function, accept_state)
    # print(eqs)
    mid_transition_function = copy.deepcopy(transition_function)
    for key in eqs:
        for key_2 in eqs:
            if eqs[key] == eqs[key_2]:
                if key != key_2:
                    for symbol in alphabet:
                        try:
                            del mid_transition_function[(key, symbol)]
                        except KeyError:
                            continue
    return states, alphabet, mid_transition_function, start_state, accept_state


if __name__ == '__main__':
    states, alphabet, transition_function, start_state, accept_state = finite_state_automata2(grammar_str8)
    mid_state, alphabet, tf, mid_start_state, mid_accept_state = (
        transition_function_deterministic(states, alphabet, transition_function, start_state, accept_state))
    states, alphabet, mid_transition_function, start_state, accept_state = automata_minimization(mid_state, alphabet, tf,
                                                                                               mid_start_state,
                                                                                               mid_accept_state)
    print(transition_function_print(mid_transition_function))

    groups = {(0,): ['Z'], (): ['BZ', 'ZAB'], (0, 1): ['ZA']}