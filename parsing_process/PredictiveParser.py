import pygraphviz as pgv


class TreeNode:
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


class PredictiveParser:
    def __init__(self, table, start):
        self.table = table
        self.start = start
        self.stack = [('#', None), (start, TreeNode(start))]  # Stack now holds tuples of (symbol, TreeNode)
        self.input_str = ""
        self.current_index = 0
        self.root = self.stack[1][1]  # Root of the syntax tree
        self.parsing_steps = ''

    def parse(self, input_str):
        self.input_str = input_str + '#'  # Add end marker
        self.current_index = 0

        step = 0
        self.parsing_steps += f"{'步骤':<10}{'栈':<30}{'输入':<30}{'动作'}\n"
        print(f"{'步骤':<10}{'栈':<30}{'输入':<30}{'动作'}")
        print("-" * 80)

        while len(self.stack) > 0:
            top, node = self.stack.pop()
            current_char = self.input_str[self.current_index]
            stack_content = ''.join(symbol for symbol, _ in reversed(self.stack))
            stack_content = stack_content[::-1]
            input_content = self.input_str[self.current_index:]

            if top == 'ε':
                step += 1
                self.parsing_steps += f"{step:<10}{stack_content:<30}{input_content:<30}弹出 ε\n"
                print(f"{step:<10}{stack_content:<30}{input_content:<30}弹出 ε")
                continue
            elif top in self.table:
                production = self.table[top].get(current_char)
                if production and production != [[]]:
                    step += 1
                    action = f"用 {top} -> {''.join([''.join(p) for p in production])}"
                    self.parsing_steps += f"{step:<10}{stack_content:<30}{input_content:<30}{action}\n"
                    print(f"{step:<10}{stack_content:<30}{input_content:<30}{action}")
                    children_nodes = []
                    for symbol in reversed(production[0]):
                        child_node = TreeNode(symbol)
                        children_nodes.append(child_node)
                        self.stack.append((symbol, child_node))
                    node.children.extend(reversed(children_nodes))
                else:
                    self.parsing_steps += f"Error: No production found for table[{top}][{current_char}]\n"
                    print(f"Error: No production found for table[{top}][{current_char}]")
                    return False
            else:
                if top == current_char:
                    step += 1
                    action = f"匹配 {top}"
                    self.parsing_steps += f"{step:<10}{stack_content:<30}{input_content:<30}{action}\n"
                    print(f"{step:<10}{stack_content:<30}{input_content:<30}{action}")
                    if node:  # If the node is not None (it would be None for '#')
                        leaf_node = TreeNode(top)
                        node.add_child(leaf_node)
                    if top == '#':
                        return True
                    self.current_index += 1
                else:
                    self.parsing_steps += f"Error: Expected {top}, but found {current_char}\n"
                    print(f"Error: Expected {top}, but found {current_char}")
                    return False

        if self.current_index == len(self.input_str) - 1:  # Check if all input is consumed
            print("Parsing successful!")
            return True
        else:
            self.parsing_steps += f"Error: Input not fully consumed, index at {self.current_index}\n"
            print(f"Error: Input not fully consumed, index at {self.current_index}")
            return False

    def print_syntax_tree(self, node=None, indent=""):
        if node is None:
            node = self.root
        print(indent + node.symbol)
        for child in node.children:
            self.print_syntax_tree(child, indent + "  ")

    def draw_syntax_tree(self, filename="syntax_tree.png"):
        graph = pgv.AGraph(strict=False, directed=True)
        self._add_nodes_edges(graph, self.root)
        graph.layout(prog='dot')
        graph.draw(filename)

    def _add_nodes_edges(self, graph, node, parent_name=None):
        node_name = str(id(node))
        graph.add_node(node_name, label=node.symbol)
        if parent_name:
            graph.add_edge(parent_name, node_name)
        for child in node.children:
            self._add_nodes_edges(graph, child, node_name)


# 调用解析器并绘制语法树的函数
def parse_and_draw(input_str, parsing_table, start_symbol, output_file="syntax_tree.png"):
    parser = PredictiveParser(parsing_table, start_symbol)
    result = parser.parse(input_str)
    print(f"Result: {'Success' if result else 'Failure'}")

    # 打印语法树
    parser.print_syntax_tree()

    # 绘制语法树
    parser.draw_syntax_tree(output_file)
    print(f"Syntax tree saved to {output_file}")


if __name__ == "__main__":
    # 语法分析表
    parsing_table = {
        'E': {
            '(': [['T', "E'"]],
            'i': [['T', "E'"]],
            '+': [],
            '*': [],
            ')': [],
            '#': [],
        },
        'T': {
            '(': [['F', "T'"]],
            'i': [['F', "T'"]],
            '+': [],
            '*': [],
            ')': [],
            '#': [],
        },
        'F': {
            '(': [['(', 'E', ')']],
            'i': [['i']],
            '+': [],
            '*': [],
            ')': [],
            '#': [],
        },
        "E'": {
            '+': [['+', 'T', "E'"]],
            ')': [['ε']],
            '#': [['ε']],
            '*': [],
            '(': [],
            'i': [],
        },
        "T'": {
            '+': [['ε']],
            '*': [['*', 'F', "T'"]],
            ')': [['ε']],
            '#': [['ε']],
            '(': [],
            'i': [],
        }
    }
    start_symbol = 'E'

    # 调用函数解析字符串并绘制语法树
    parse_and_draw("(i+i)*i", parsing_table, start_symbol, "syntax_tree.png")

