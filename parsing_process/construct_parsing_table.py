from derivation_visualizer.extract_grammar import GrammaticalQuadrupleExtraction


def calculate_first(terminators, non_terminators, production):
    first = {symbol: set() for symbol in non_terminators}

    def calculate_symbol_first(symbol):
        for production_rule in production[symbol]:
            # print("symbol and production_rule: ",symbol,production_rule)
            if production_rule[0] in terminators or production_rule[0] == 'ε':
                first[symbol].add(production_rule[0])
                continue
            elif production_rule[0] in non_terminators:
                mid_production_rule = production[production_rule[0]]
                if mid_production_rule[0] in terminators:
                    first[symbol] |= {mid_production_rule[0]}
                else:
                    for element in production_rule:
                        if element in terminators:
                            first[symbol] |= {element}
                            break
                        if element in non_terminators:
                            mid_first = calculate_symbol_first(element)
                            if 'ε' not in mid_first:
                                first[symbol] |= calculate_symbol_first(element)
                                break
                            first[symbol] |= calculate_symbol_first(element)

        return first[symbol]

    for symbol in non_terminators:
        calculate_symbol_first(symbol)

    return first


def calculate_follow(start, terminators, non_terminators, production, first):
    follow = {symbol: set() for symbol in non_terminators}
    follow[start].add('#')

    def calculate_symbol_follow(symbol):
        for head, body in production.items():
            for rule in body:
                for i, element in enumerate(rule):
                    if element == symbol:
                        if i == len(rule) - 1:
                            follow[symbol] |= follow[head]
                            break

                        remaining_symbols = rule[i + 1:]

                        for next_symbol in remaining_symbols:
                            if next_symbol in terminators:
                                follow[symbol].add(next_symbol)
                                break
                            elif 'ε' not in first[next_symbol]:
                                follow[symbol] |= first[next_symbol]
                                break
                            else:
                                follow[symbol] |= first[next_symbol] - {'ε'}
                                follow[symbol] |= calculate_symbol_follow(head)

        return follow[symbol]

    for symbol in non_terminators:
        calculate_symbol_follow(symbol)

    return follow


def construct_parsing_table(terminators, non_terminators, production, first, follow):
    parsing_table = {non_terminal: {terminator: [] for terminator in terminators + ['#']} for non_terminal in
                     non_terminators}

    for head, bodies in production.items():
        for body in bodies:
            first_set = set()
            if body[0] == 'ε':
                first_set = {'ε'}
            else:
                for symbol in body:
                    if symbol in terminators:
                        first_set.add(symbol)
                        break
                    first_set |= first[symbol]
                    if 'ε' not in first[symbol]:
                        break
                    first_set.discard('ε')

            for terminal in first_set:
                if terminal != 'ε':
                    parsing_table[head][terminal].append(body)

            if 'ε' in first_set or body[0] == 'ε':
                for terminal in follow[head]:
                    parsing_table[head][terminal].append(body)

    return parsing_table


if __name__ == '__main__':
    from data.grammar import grammar_str2

    # 示例用法
    extractor = GrammaticalQuadrupleExtraction()
    grammar_string = grammar_str2

    print("原始文法: \n"+grammar_string)
    non_terminators, terminators, production, start = extractor.extract_grammar_components(grammar_string)

    print("消除左递归：")
    non_terminators = ['E', 'T', 'F', "E'", "T'"]
    mid_production = {'E': [['T', "E'"]], 'T': [['F', "T'"]], 'F': [['i'], ['(', "E", ")"]],
                      "E'": [['ε'], ['+', "T", "E'"]], "T'": [['ε'], ['*', "F", "T'"]]}

    print("terminators: ", terminators)
    print("non_terminators: ", non_terminators)
    print("production: ", mid_production)
    print("start: ", start)

    first = calculate_first(terminators, non_terminators, mid_production)
    print("\nFirst 集合:")
    for symbol, first_set in first.items():
        print(symbol, ":", first_set)

    follow = calculate_follow(start, terminators, non_terminators, mid_production, first)
    print("\nFollow 集合:")
    for symbol, follow_set in follow.items():
        print(symbol, ":", follow_set)

    parsing_table = construct_parsing_table(terminators, non_terminators, mid_production, first, follow)

    print("\n预测分析表:")
    print("{:<10} {:<10} {:<10}".format("非终结符", "终结符", "产生式"))
    for non_terminal, terminals in parsing_table.items():
        for terminal, rules in terminals.items():
            if rules:
                print("{:<12} {:<12} {:<10}".format(str(non_terminal), str(terminal), ''.join(rules[0])))

    print("First:\n", first)
    print("Follow:\n", follow)
    print("Parsing Table:\n", parsing_table)
    # first = {'E': {'i', '('}, 'T': {'i', '('}, 'F': {'i', '('}, "E'": {'ε', '+'}, "T'": {'ε', '*'}}
    # follow = {'E': {')', '#'}, 'T': {'#', '+', ')'}, 'F': {'#', '+', ')', '*'},
    #           "E'": {')', '#'}, "T'": {'#', '+', ')'}}
    # parsing_table = {'E': {'+': [], '*': [], '(': [['T', "E'"]], ')': [], 'i': [['T', "E'"]], '#': []},
    #                  'T': {'+': [], '*': [], '(': [['F', "T'"]], ')': [], 'i': [['F', "T'"]], '#': []},
    #                  'F': {'+': [], '*': [], '(': [['(', 'E', ')']], ')': [], 'i': [['i']], '#': []},
    #                  "E'": {'+': [['+', 'T', "E'"]], '*': [], '(': [], ')': [['ε']], 'i': [], '#': [['ε']]},
    #                  "T'": {'+': [['ε']], '*': [['*', 'F', "T'"]], '(': [], ')': [['ε']], 'i': [], '#': [['ε']]}}