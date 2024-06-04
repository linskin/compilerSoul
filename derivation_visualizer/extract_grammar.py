import data.grammar


class GrammaticalQuadrupleExtraction:
    def __init__(self):
        self.__production = {}
        self.__start = ''
        self.__terminators = []
        self.__non_terminators = []

    @staticmethod
    def __extract_from_line(s):
        left, right = s.split('::=')
        return left.strip(), right.strip()

    @staticmethod
    def __clean_list(lis):
        mid_lis = lis.copy()
        tag = True
        while tag:
            tag = False
            for item in mid_lis:
                if item == '':
                    tag = True
                    mid_lis.remove(item)
        return mid_lis

    def __add_production(self, non_terminal, oneproduction):
        if non_terminal in self.__production:
            self.__production[non_terminal].append(oneproduction)
        else:
            self.__production[non_terminal] = [oneproduction]

    def __extract_rules_from_left_and_right_part(self, ls, rs):
        if ls not in self.__terminators:
            self.__terminators.append(ls)
        if self.__start == '':
            self.__start = ls
        mid_re = rs.split('|')
        for item in mid_re:
            item = self.__clean_list(item.split(' '))
            item_ts = []
            for item_t in item:
                item_ts += [item_t]
            self.__add_production(ls, item_ts)

    def __extract_non_terminators_from_right_part_list(self, right_part_list):
        for item_r in right_part_list:
            mid_re = item_r.split('|')
            for item in mid_re:
                item = self.__clean_list(item.split(' '))
                for item_t in item:
                    if item_t not in self.__non_terminators and item_t not in self.__terminators:
                        self.__non_terminators.append(item_t)

    def extract_grammar_components(self, gs):
        right_part_list = []
        mid_s = self.__clean_list(gs.split("\n"))
        for item_s in mid_s:
            left, right = self.__extract_from_line(item_s)
            self.__extract_rules_from_left_and_right_part(left, right)
            right_part_list.append(right)
        self.__extract_non_terminators_from_right_part_list(right_part_list)
        return self.__terminators, self.__non_terminators, self.__production, self.__start


if __name__ == '__main__':
    # 示例用法
    extractor = GrammaticalQuadrupleExtraction()
    grammar_string2 = "Ems ::= Ems + Tfs | Tfs\nTfs ::= Tfs * F' | F'\nF' ::= ( Ems ) | iss\n\n\n\n\n"
    grammar_string = data.grammar.grammar_str7

    terminators, non_terminators, production, start = extractor.extract_grammar_components(grammar_string)
    print(terminators)
    print(non_terminators)
    print(production)
    print(start)
