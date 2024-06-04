import base64
import os
from io import BytesIO

import pygraphviz as pgv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
allowed_extensions = {'txt'}

grammarElement = {}
terSymblo = ['#']
non_ter = []
Start = 'S'
allSymbol = []  # 所有符号
firstVT = {}  # FIRSTVT集
lastVT = {}  # lastVT集
formules = []

data = dict()
sentencePattern = ["N+N", "N*N", "N/N", "(N)", "i", "N^N", "N,N", "a"]
analyzeResult = False
analyzeStep = 0
parse_tree = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def rationalize_inputs(content):
    end_content = []
    for line in content:
        line = line.replace(' ', "")
        line = line.replace('\n', "")
        if line != "":
            left, right = line.split("::=")
            items = right.split("|")
            for item in items:
                end_content += [left + " -> " + item + '\n']
    return end_content


def data_input(filepath):
    global grammarElement, terSymblo, non_ter, Start, allSymbol, firstVT, lastVT, formules
    grammarElement = {}
    terSymblo = ['#']
    non_ter = []
    Start = 'S'
    allSymbol = []  # 所有符号
    firstVT = {}  # FIRSTVT集
    lastVT = {}  # lastVT集
    formules = []

    with open(filepath, 'r+', encoding="utf-8") as f:
        temp = f.readlines()
    temp = rationalize_inputs(temp)
    for i in temp:
        line = str(i.strip("\n"))
        formules.append(line)
        if line[0] not in non_ter:
            non_ter.append(line[0])
            grammarElement.setdefault(line[0], line[5:])
        else:
            grammarElement[line[0]] += "|" + line[5:]
    for i in temp:
        line = str(i.strip("\n")).replace(" -> ", "")
        for j in line:
            if j not in non_ter and j not in terSymblo:
                terSymblo.append(j)
    if 'ε' in terSymblo: terSymblo.remove('ε')


def get_fistVT(formule):
    x = formule[0]
    i = 5
    if formule[i] in terSymblo and formule[i] not in firstVT[x]:  # 首位为终结符 P->a...
        firstVT[x] += formule[i]
    elif formule[i] in non_ter:  # 首位为非终结符
        for f in firstVT[formule[i]]:
            if f not in firstVT[x]:
                firstVT[x] += f
        if i + 1 < len(formule) and formule[i + 1] in terSymblo and formule[i + 1] not in firstVT[x]:  # P->Q..
            firstVT[x] += formule[i + 1]


def get_lastVT(formule):
    x = formule[0]
    i = len(formule) - 1
    if formule[i] in terSymblo and formule[i] not in lastVT[x]:
        lastVT[x] += formule[i]
    elif formule[i] in non_ter:
        for f in lastVT[formule[i]]:
            if f not in lastVT[x]:
                lastVT[x] += f
        if formule[i - 1] in terSymblo and formule[i - 1] not in lastVT[x]:
            lastVT[x] += formule[i - 1]


def addtomydict(thedict, key_a, key_b, val):
    if key_a in thedict.keys():
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a: {key_b: val}})


def analy(formule):
    start = 5
    end = len(formule) - 2
    if start == end: return
    for i in range(start, end):
        if formule[i] in terSymblo and formule[i + 1] in terSymblo:
            addtomydict(data, formule[i], formule[i + 1], "=")
        if formule[i] in terSymblo and formule[i + 1] in non_ter and formule[i + 2] in terSymblo:
            addtomydict(data, formule[i], formule[i + 2], "=")
        if formule[i] in terSymblo and formule[i + 1] in non_ter:
            for j in firstVT[formule[i + 1]]:
                addtomydict(data, formule[i], j, "<")
        if formule[i] in non_ter and formule[i + 1] in terSymblo:
            for j in lastVT[formule[i]]:
                addtomydict(data, j, formule[i + 1], ">")
        if formule[i + 1] in terSymblo and formule[i + 2] in non_ter:
            for j in firstVT[formule[i + 2]]:
                addtomydict(data, formule[i + 1], j, "<")
        if formule[i + 1] in non_ter and formule[i + 2] in terSymblo:
            for j in lastVT[formule[i + 1]]:
                addtomydict(data, j, formule[i + 2], ">")


def reverseString(string):
    return string[::-1]


def findVTele(string):
    ele = '\0'
    ele_index = 0
    for i in range(len(string)):
        if string[i] in terSymblo:
            ele = string[i]
            ele_index = i
    return ele, ele_index


def initStack(string):
    global analysis_steps, parse_tree
    parse_tree = pgv.AGraph(strict=False, directed=True)
    analysis_steps = []  # 清空分析步骤
    analysisStack = "#"
    currentStack = reverseString(string)
    toAnalyze(analysisStack, currentStack)


def toAnalyze(analysisStack, currentStack):
    global analyzeResult, analyzeStep, parse_tree, node_counter
    analyzeStep += 1
    analysisStack_top, analysisStack_index = findVTele(analysisStack)
    currentStack_top = currentStack[-1]
    relation = data.get(analysisStack_top, {}).get(currentStack_top, None)

    analysis_steps.append({
        'step': analyzeStep,
        'analysis_stack': analysisStack,
        'current_stack': currentStack,
        'relation': relation
    })

    if relation == '<':
        analysisStack += currentStack_top
        currentStack = currentStack[:-1]
        toAnalyze(analysisStack, currentStack)
    elif relation == '>':
        currentChar = analysisStack_top
        temp_string = ""
        reduction_list = []
        for i in range(len(analysisStack) - 1, -1, -1):
            if analysisStack[i].isupper():
                temp_string = analysisStack[i] + temp_string
                continue
            elif data.get(analysisStack[i], {}).get(currentChar) == '<':
                break
            temp_string = analysisStack[i] + temp_string
            reduction_list.append(analysisStack[i])
            currentChar = analysisStack[i]
        if temp_string in sentencePattern:
            parent_node = f"N{analyzeStep}"
            parse_tree.add_node(parent_node)
            for symbol in reversed(reduction_list):
                child_node = f"{symbol}_{analyzeStep}"
                parse_tree.add_node(child_node)
                parse_tree.add_edge(parent_node, child_node)
            analysisStack = analysisStack[:i + 1] + 'N'
            toAnalyze(analysisStack, currentStack)
        else:
            analyzeResult = False
            return
    elif relation == '=':
        if analysisStack_top == '#' and currentStack_top == '#':
            analyzeResult = True
            return
        else:
            analysisStack += currentStack_top
            currentStack = currentStack[:-1]
            toAnalyze(analysisStack, currentStack)
    elif relation is None:
        analyzeResult = False
        return


def save_parse_tree():
    img = BytesIO()
    parse_tree.layout(prog='dot')
    parse_tree.draw(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.read()).decode('utf-8')
    return img_base64


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        data_input(filepath)
        for i in non_ter:
            firstVT.setdefault(i, "")
            lastVT.setdefault(i, "")
        for i in terSymblo:
            for j in terSymblo:
                addtomydict(data, i, j, '')
        for n in range(10):
            for i in formules:
                get_fistVT(i)
                get_lastVT(i)
        temp2 = Start + " -> #" + Start + "#"
        formules.append(temp2)
        for i in formules:
            analy(i)
        return redirect(url_for('show_results'))
    return redirect(request.url)


@app.route('/results')
def show_results():
    firstvt = {i: firstVT[i] for i in non_ter}
    lastvt = {i: lastVT[i] for i in non_ter}
    precedence_table = {i: {j: data[i][j] if j in data[i] else '' for j in terSymblo} for i in terSymblo}
    return render_template('results.html', firstvt=firstvt, lastvt=lastvt, precedence_table=precedence_table)


@app.route('/analyze', methods=['POST'])
def analyze_string():
    global analyzeResult, analyzeStep, analysis_steps
    analyzeResult = False
    analyzeStep = 0
    analysis_steps = []  # 清空分析步骤
    string = request.form['input_string']
    string = string.replace(" ", "")
    string += "#"
    initStack(string)
    parse_tree_base64 = save_parse_tree()
    return render_template('analyze.html', analyze_result=analyzeResult, steps=analyzeStep,
                           analysis_steps=analysis_steps, parse_tree_base64=parse_tree_base64)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
