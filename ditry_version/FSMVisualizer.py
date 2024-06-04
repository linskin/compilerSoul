import graphviz
import ipywidgets as widgets
from IPython.display import display

from FiniteAutomaton import construct_fsm
from FiniteStateAutomata2 import FiniteStateAutomata2


class FSMVisualizer:
    def __init__(self, grammar_str):
        self.grammar_str = grammar_str

    def visualize(self):
        # Extract components and construct FSM
        fsa = FiniteStateAutomata2(self.grammar_str)
        states, alphabet, transition_function, start_state, accept_state = fsa.extract_components()
        mid_state, new_tf, mid_accept_state = fsa.construct_fsm()
        fsm = construct_fsm(mid_state, alphabet, transition_function, start_state, mid_accept_state)

        # Create visualization of FSM
        dot = graphviz.Digraph()
        for state in fsm.states:
            dot.node(state, shape='circle', style='filled', fillcolor='lightblue')
        for transition, next_states in fsm.transition_function.items():
            for next_state in next_states:
                dot.edge(transition[0], next_state, label=transition[1])

        # Display input grammar, grammatical quadruple, and FSM graph
        display(widgets.VBox([
            widgets.HTML('<h2>Input Grammar:</h2><pre>{}</pre>'.format(self.grammar_str)),
            widgets.HTML('<h2>Grammatical Quadruple:</h2><pre>{}</pre>'.format(fsa.print_transition_function())),
            widgets.Image(value=dot.pipe(format='png')),
        ]))


if __name__ == '__main__':
    # Example usage:
    grammar_str8 = ("Z ::= Z a | A a | B b\n"
                    "A ::= B a | Z a | a\n"
                    "B ::= A b | B a | b")

    visualizer = FSMVisualizer(grammar_str8)
    visualizer.visualize()