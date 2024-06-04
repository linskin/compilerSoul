import pygraphviz as pgv
import io
import base64
import matplotlib.pyplot as plt
from PIL import Image as PILImage

def generate_transition_graph(transition_function):
    G = pgv.AGraph(directed=True)
    G.graph_attr['rankdir'] = 'LR'  # 设置图的方向为从左到右
    for (source, symbol), destinations in transition_function.items():
        for destination in destinations:
            G.add_edge(source, destination, label=symbol)
    return G

def draw_transition_graph(transition_function):
    G = generate_transition_graph(transition_function)
    G.layout(prog="dot")

    # 将图像保存到字节流中
    img_stream = io.BytesIO()
    G.draw(img_stream, format='png')
    img_stream.seek(0)

    # 将图像字节流转换为base64编码
    img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')
    return img_base64

# 更复杂的测试用例
transition_function = {
    ('q0', '0'): {'q0', 'q1'},
    ('q0', '1'): {'q0'},
    ('q1', '0'): {'q2'},
    ('q1', '1'): {'q2', 'q3'},
    ('q2', '0'): {'q3'},
    ('q2', '1'): {'q0'},
    ('q3', '0'): {'q1'},
    ('q3', '1'): {'q2', 'q3'},
    ('q4', '0'): {'q0'},
    ('q4', '1'): {'q1'}
}

# 生成base64图像
base64_image = draw_transition_graph(transition_function)

# 解码并显示图像
img_data = base64.b64decode(base64_image)
img = PILImage.open(io.BytesIO(img_data))

# 显示图像
plt.figure(figsize=(12, 6))  # 调整图形尺寸，确保横向显示
plt.imshow(img)
plt.axis('off')  # 隐藏坐标轴
plt.show()

# 保存图像到文件
img.save("transition_graph.png")
