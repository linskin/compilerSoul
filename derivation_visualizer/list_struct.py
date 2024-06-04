# 创建一个包含字符串的列表
string_list = [
    ["apple", "banana", "cherry"],
    ["orange", "grape", "kiwi"],
    ["melon", "strawberry", "pineapple"]
]

# 访问列表中的元素
print(string_list[0][0])  # 输出第一行第一列的元素
print(string_list[1][2])  # 输出第二行第三列的元素
# 增加新的行
string_list.append(["pear", "blueberry", "raspberry"])
print(string_list)
# print("".join(string_list[2]))
# 在特定行增加新的元素
string_list[0].append("apricot")
print(string_list)
# 删除特定行
del string_list[1]
print(string_list)

# 删除特定索引处的元素
string_list[0].pop(0)
print(string_list)
# 修改特定位置的元素
string_list[2][1] = "mango"
print(string_list)

# 两个列表
rows = ["row1", "row2", "row3"]
columns = ["col1", "col2", "col3"]

# 使用嵌套字典表示行和列
matrix = {row_label: {col_label: None for col_label in columns} for row_label in rows}

# 将列表分别变成行和列
for i, row_label in enumerate(rows):
    for j, col_label in enumerate(columns):
        matrix[row_label][col_label] = f"{row_label}_{col_label}"

# 输出结果
for row_label, row_data in matrix.items():
    print(row_label, ": ", row_data)

import pandas as pd

# 两个列表
rows = ["row1", "row2", "row3"]
columns = ["col1", "col2", "col3"]

# 使用 Pandas 将列表转换为 DataFrame
df = pd.DataFrame(index=rows, columns=columns)

# 将列表分别变成行和列
for i, row_label in enumerate(rows):
    for j, col_label in enumerate(columns):
        df.at[row_label, col_label] = f"{row_label}_{col_label}"

# 输出结果
print(df)
