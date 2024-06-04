import copy

from print_productions import print_productions


class GrammarCleaner:
    def __init__(self):
        pass

    @staticmethod
    def add_to_prod_dict(s, t, p):
        if s not in p:
            p[s] = [t]
        else:
            p[s].append(t)

    @staticmethod
    def clean_UtoU(production):
        cleaned_production = {}
        for key, value in production.items():
            for item in value:
                if key not in item or len(item) >= 2:
                    GrammarCleaner().add_to_prod_dict(key, item, cleaned_production)
        # print(print_productions(cleaned_production))
        # print("UU")
        return cleaned_production

    @staticmethod
    def clean_Utou1(production, start, terminators):
        end_production = copy.deepcopy(production)
        marks = [start]
        # start_list = end_production[start]
        # for item in start_list:
        #     for item_s in item:
        #         if item_s in terminators and item_s not in marks:
        #             # print(item_s)
        #             marks.append(item_s)
        tag1 = True
        tag3 = True
        while tag1:
            tag1 = False
            for key in marks:
                k_list = end_production[key]
                for item in k_list:
                    for item_s in item:
                        if item_s in terminators and item_s not in marks:
                            tag1 = True
                            marks.append(item_s)
        for key in end_production.copy():
            if key not in marks:
                tag3 = False
                del end_production[key]
        # print(print_productions(end_production))
        # print("Uu1")
        return end_production, tag3

    def clean_Utou2(self, production, terminators):
        end_production = {}
        marks = []
        tag2 = True
        for key in production:
            for item in production[key]:
                tag = True
                for item_s in item:
                    if item_s in terminators:
                        tag = False
                        break
                if tag:
                    tag2 = False
                    marks.append(key)
                    self.add_to_prod_dict(key, item, end_production)
        tag1 = True
        while tag1:
            tag1 = False
            for key in production:
                for item in production[key]:
                    num_no_mark = False
                    for item_s in item:
                        if item_s in terminators and item_s not in marks:
                            num_no_mark = True
                            break
                    if not num_no_mark and (key not in end_production or item not in end_production[key]):
                        tag1 = True
                        marks.append(key)
                        self.add_to_prod_dict(key, item, end_production)
        # print(print_productions(end_production))
        # print("Uu2")
        return end_production, tag2

    def auto_clean(self, production, start, terminators):
        end_production = self.clean_UtoU(production)
        tag = True
        while tag:
            end_production, flg = self.clean_Utou1(end_production, start, terminators)
            if flg:
                tag = False
            end_production, flg = self.clean_Utou2(end_production, terminators)
            if flg:
                tag = False
        return end_production


if __name__ == '__main__':
    cleaner = GrammarCleaner()
    productions3 = {'Z': ['Be'], 'A': ['Ae', 'e'], 'B': ['Ce', 'Af'], 'C': ['Cf']}
    productions4 = {'Ems': [['Ems', '+', 'Tfs'], ['Tfs']], 'Tfs': [['Tfs', '*', "F'"], ["F'"]],
                    "F'": [['(', 'Ems', ')'], ['i']]}
    productions2 = {'Z': [['B', 'e']], 'A': [['A', 'e'], ['e']], 'B': [['C', 'e'], ['A', 'f']], 'C': [['C', 'f']],
                   'D': [['f']], 'E': [['E']]}
    productions = {'Z': [['E', '+', 'T']],
                   'E': [['E'], ['S', '+', 'F'], ['T']],
                   'F': [['F'], ['F', 'P'], ['P']],
                   'P': [['G']],
                   'G': [['G'], ['G', 'G'], ['F']],
                   'T': [['T', '*', 'i'], ['i']],
                   'Q': [['E'],['E', '+', 'F'], ['T'], ['S']],
                   'S': [['i']]}
    # print(cleaner.clean_UtoU(productions))
    # print(cleaner.clean_Utou1(productions, start='Z', terminators=['Z', 'E', 'F', 'P', 'G', 'T', 'Q', 'S']))
    # print(cleaner.clean_Utou2(productions, terminators=['Z', 'E', 'F', 'P', 'G', 'T', 'Q', 'S']))
    # print(cleaner.auto_clean(productions, start='Z', terminators=['Z', 'E', 'F', 'P', 'G', 'T', 'Q', 'S']))
    print(print_productions(cleaner.auto_clean(productions, start='Z', terminators=['Z', 'E', 'F', 'P', 'G', 'T', 'Q', 'S'])))
    # print(print_productions(cleaner.auto_clean(productions, start='Z', terminators=['Z', 'A','B','C'])))
