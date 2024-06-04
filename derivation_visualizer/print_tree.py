import copy


def insert_separator_uniformly(lst):
    n = len(lst)
    new_lst = [None] * (2 * n - 1)  # 创建一个新列表，长度为2n-1

    # 将原列表中的元素和23交替插入新列表中
    for i in range(n):
        new_lst[i * 2] = lst[i]
        if i < n - 1:
            new_lst[i * 2 + 1] = '_' * 4

    return new_lst


def generate_tree(tree, start):
    mid_tree = copy.deepcopy(tree)
    pre_string = ["_" * 4] + [start]
    result = ''.join(pre_string) + '\n'
    tag = True
    while tag:
        tag = False
        j = 0
        for i in range(len(pre_string)):
            if pre_string[i] == '_' * 4:
                continue
            j += 1
            if pre_string[i] in mid_tree:
                tag = True
                try:
                    item_left, item_rigth = mid_tree[pre_string[i]][0]
                except IndexError:
                    return result
                if j == item_left:
                    mid_tree[pre_string[i]].pop(0)
                    pre_string[i:i + 1] = insert_separator_uniformly(item_rigth)
                    break
        result += ''.join(pre_string) + '\n'
    return result


if __name__ == '__main__':
    print("语法分析树：")
    start2 = 'E'
    start = 'Ems'
    tree_list2 = {
        'E': [[1, ['E', '+', 'T']], [1, ['E', '+', 'T']], [1, ['E', '+', 'T']], [1, ['T']], [12, ['E', '+', 'T']],
              [12, ['T']]],
        'T': [[1, ['F']], [3, ['F']], [5, ['T', '*', 'F']], [5, ['T', '*', 'F']], [5, ['F']], [11, ['F']], [12, ['F']],
              [14, ['T', '*', 'F']], [14, ['F']]],
        'F': [[1, ['i']], [3, ['i']], [5, ['i']], [7, ['i']], [9, ['i']], [11, ['(', 'E', ')']], [12, ['i']],
              [14, ['i']], [16, ['i']]]}
    tree_list3 = {'Ems': [[1, ['Ems', '+', 'Tfs']],
                         [1, ['Ems', '+', 'Tfs']],
                         [1, ['Tfs']]],
                 'Tfs': [[1, ["F'"]],
                         [3,["F'"]],
                         [5, ["F'"]]],
                 "F'": [[1, ['iss']],
                        [3, ['iss']],
                        [5, ['iss']]]
                 }
    tree_list = {'Ems': [[1, ['Ems', '+', 'Tfs']], [1, ['Tfs']]], 'Tfs': [[1, ['Tfs', '*', "F'"]], [1, ["F'"]]]}
    ans = generate_tree(tree_list, start)
    print(ans)
