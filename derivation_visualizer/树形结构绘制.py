
import matplotlib.pyplot as plt
import networkx as nx

# 创建树形结构
tree = nx.DiGraph()
tree.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4)])

# 绘制树形结构
pos = nx.spring_layout(tree)  # 定义节点位置
nx.draw(tree, pos, with_labels=True, node_size=1000, node_color="lightblue", font_size=10)
plt.show()

import pygraphviz as pgv

# 创建树形结构
tree = pgv.AGraph(strict=False, directed=True)
tree.add_edge(0, 1)
tree.add_edge(0, 2)
tree.add_edge(1, 3)
tree.add_edge(1, 4)

# 绘制树形结构
tree.layout(prog="dot")  # 设置布局
tree.draw("tree_graphviz.png")

# import spacy
# python -m spacy download en_core_web_sm
# python -m spacy download zh_core_web_sm

import matplotlib.pyplot as plt
import networkx as nx

# 创建树形结构
tree = nx.DiGraph()
tree.add_edges_from([("Root", "Child1"), ("Root", "Child2"), ("Child1", "Grandchild1"), ("Child1", "Grandchild2")])

# 绘制树形结构
pos = nx.spring_layout(tree)  # 定义节点位置
nx.draw(tree, pos, with_labels=True, node_size=1000, node_color="lightblue", font_size=10)
plt.show()

import pygraphviz as pgv

# 创建树形结构
tree = pgv.AGraph(strict=False, directed=True)
tree.add_edge("Root", "Child1")
tree.add_edge("Root", "Child2")
tree.add_edge("Child1", "Grandchild1")
tree.add_edge("Child1", "Grandchild2")

# 绘制树形结构
tree.layout(prog="dot")  # 设置布局
tree.draw("tree_graphviz.png")

import pygraphviz as pgv

# 创建树形结构
tree = pgv.AGraph(strict=False, directed=True)
tree.add_edge("Root", "Child1")
tree.add_edge("Root", "Child2")
tree.add_edge("Child1", "Grandchild1")
tree.add_edge("Child1", "Grandchild2")

# 绘制树形结构
tree.layout(prog="dot")  # 设置布局
tree.draw("tree_graphviz.png")
