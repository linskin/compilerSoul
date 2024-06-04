import base64
import tempfile

import matplotlib.pyplot as plt
import networkx as nx

from finite_automaton.compresses import automata_minimization
from finite_automaton.deterministic import transition_function_deterministic
from finite_automaton.five_part_extract import finite_state_automata2, grammar_str8
from finite_automaton.graph_draw import draw_transition_graph


class FiniteAutomaton:
    def __init__(self, K, sigma, M, S, F):
        self.states = set(K)  # 状态集合
        self.alphabet = set(sigma)  # 输入字母表
        self.transitions = M  # 状态转移函数
        self.start_state = S[0]  # 初始状态
        self.accept_states = set(F)  # 接受状态集合
        self.result = {}
    def run(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if (current_state, symbol) in self.transitions:
                mid_state = self.transitions[(current_state, symbol)]
                current_state = mid_state[0]
            else:
                return False
        return current_state in self.accept_states

    def construct_fsm(self):
        return self

    def generate_transition_graph(self):
        G = nx.DiGraph()

        for state in self.states:
            G.add_node(state)

        for (source, symbol), destinations in self.transitions.items():
            for destination in destinations:
                G.add_edge(source, destination, label=symbol)

        return G

    def draw_transition_graph(self):
        G = self.generate_transition_graph()

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold",
                arrowsize=20)
        edge_labels = {}
        for (source, symbol), destinations in self.transitions.items():
            for destination in destinations:
                if (source, destination) in edge_labels:
                    edge_labels[(source, destination)] += f", {symbol}"
                else:
                    edge_labels[(source, destination)] = symbol
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            plt.savefig(f.name, format='png')
            image_path = f.name

        with open(image_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')

        return image_base64


if __name__ == '__main__':
    states, alphabet, transition_function, start_state, accept_state = finite_state_automata2(grammar_str8)
    mid_state, alphabet, tf, mid_start_state, mid_accept_state = (
        transition_function_deterministic(states, alphabet, transition_function, start_state, accept_state))
    states, alphabet, mid_transition_function, start_state, accept_state = automata_minimization(mid_state, alphabet,
                                                                                                 tf,
                                                                                                 mid_start_state,
                                                                                                 mid_accept_state)
    fsm = FiniteAutomaton(states, alphabet, mid_transition_function, start_state, accept_state)

    test_strings = ['ba', 'babb', 'babbabb', 'aaaa', 'baa', 'babaa']

    html_output = """
    <html>
    <head>
        <title>Finite State Automaton Output</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
                background-color: #f2f2f2;
                overflow: auto;
            }
            h2 {
                color: #333333;
            }
            ul {
                list-style-type: none;
                padding-left: 0;
            }
            li {
                margin-bottom: 10px;
            }
            .container {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
            }
            .nav {
                flex: 0 0 100%;
            }
            .content {
                flex: 0 0 100%;
            }
            .graph {
                border: 2px solid #cccccc;
                padding: 10px;
                margin-bottom: 20px;
                background-color: #ffffff;
                max-width: 600px;
            }
            .hidden {
                display: none;
            }
            @keyframes fadeIn {
              from {
                opacity: 0;
              }
              to {
                opacity: 1;
              }
            }
            .graph:hover {
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
            }
        </style>
        <script>
            function toggleContent(id) {
                var content = document.getElementById(id);
                if (content.classList.contains("hidden")) {
                    content.classList.remove("hidden");
                } else {
                    content.classList.add("hidden");
                }
            }
        </script>
    </head>
    <body>
    """

    html_output += "<h1>Finite State Automaton Output</h1>"
    html_output += "<div class='container'>"
    html_output += "<div class='nav'>"
    html_output += "<ul style='justify-content: space-around; list-style: list-style-type; padding: 0;'>"
    html_output += "<li><a href='#' onclick=\"toggleContent('grammar')\">Grammar</a></li>"
    html_output += "<li><a href='#' onclick=\"toggleContent('states')\">States</a></li>"
    html_output += "<li><a href='#' onclick=\"toggleContent('alphabet')\">Alphabet</a></li>"
    html_output += "<li><a href='#' onclick=\"toggleContent('transition_function')\">Transition Function</a></li>"
    html_output += "<li><a href='#' onclick=\"toggleContent('start_state')\">Start State</a></li>"
    html_output += "<li><a href='#' onclick=\"toggleContent('accept_state')\">Accept State</a></li>"
    html_output += "<li><a href='#' onclick=\"toggleContent('transition_graph')\">Transition Function Graph</a></li>"
    html_output += "<li><a href='#' onclick=\"toggleContent('test_results')\">Test Results</a></li>"
    html_output += "</ul>"
    html_output += "</div>"
    html_output += "<div class='content'>"

    html_output += "<div id='grammar'>"
    html_output += "<h2>Grammar:</h2>"
    html_output += "<div class='graph'>"
    grammar_lines = grammar_str8.split('\n')
    for line in grammar_lines:
        html_output += "<li>" + line + "</li>"
    html_output += "</div></div>"

    html_output += "<div id='states'><h2>States:</h2>"
    html_output += "<div class='graph'>{" + ', '.join(states) + "}</div></div>"

    html_output += "<div id='alphabet'><h2>Alphabet:</h2>"
    html_output += "<div class='graph'>{" + ', '.join(alphabet) + "}</div></div>"

    html_output += "<div id='transition_function'><h2>Transition Function:</h2>"
    html_output += "<div class='graph'>"
    for (source, symbol), destinations in mid_transition_function.items():
        html_output += "<li>(" + source + ", " + symbol + ") -> {" + ', '.join(destinations) + "}</li>"
    html_output += "</div></div>"

    html_output += "<div id='start_state'><h2>Start State:</h2>"
    html_output += "<div class='graph'>{" + ','.join(start_state) + "}</div></div>"

    html_output += "<div id='accept_state'><h2>Accept State:</h2>"
    html_output += "<div class='graph'>{" + ', '.join(accept_state) + "}</div></div>"

    html_output += "<div id='transition_graph'><h2>Transition Function Graph:</h2>"
    html_output += "<div class='graph'>"
    html_output += f'<img src="data:image/png;base64,{draw_transition_graph(mid_transition_function)}" class="graph" style="max-width: 600px;"/>'
    html_output += "</div></div>"

    html_output += "<div id='test_results'><h2>Test Strings and Results:</h2>"
    html_output += "<div class='graph'><ul>"
    for s in test_strings:
        html_output += "<h5>String '" + s + "' matches: " + str(fsm.run(s)) + "</h5>"
    html_output += "</ul></div></div>"

    html_output += "</div></div></body></html>"

    with open("fsm_output.html", "w") as f:
        f.write(html_output)

    print("Output saved to fsm_output.html")
    import webbrowser

    # Open the HTML file in the default web browser
    webbrowser.open("fsm_output.html")
