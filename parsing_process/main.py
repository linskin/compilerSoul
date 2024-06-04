from parsing_process.PredictiveParser import PredictiveParser
from parsing_process.construct_parsing_table import *

if __name__ == "__main__":
    from data.grammar import grammar_str2

    # 示例用法
    extractor = GrammaticalQuadrupleExtraction()
    grammar_string = grammar_str2

    print("原始文法: \n" + grammar_string)
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

    parser = PredictiveParser(parsing_table, start)
    result = parser.parse("(i+i)*i")
    print(f"Result: {'Success' if result else 'Failure'}")

    # 绘制语法树
    parser.draw_syntax_tree("syntax_tree.png")
