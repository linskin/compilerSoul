def print_productions(productions):
    result = ""
    for key in productions:
        tss = ""
        for item in productions[key]:
            for item_s in item:
                tss += item_s + ' '
            tss += '| '
        result += f"{key} ::= {tss[:-2]}\n"
    return result[:-1]


if __name__ == "__main__":
    production2 = {'S': [['S', 'a'], ['T', 'b', 'c'], ['T', 'd']], 'T': [['S', 'e'], ['g', 'h']]}
    production = {'Tfs': [["F'"], ['Tfs', '*', "F'"]], "F'": [['i'], ['(', 'Ems', ')']],
                  'Ems': [['Tfs'], ['Ems', '+', 'Tfs']]}
    ans = print_productions(production)
    print(ans)
