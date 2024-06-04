import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

from eliminate_left_recursion import auto_eliminate_left_recursion
from tools.banner import banner_str, banner_str_welcome
from parsing_process.PredictiveParser import PredictiveParser
from parsing_process.construct_parsing_table import GrammaticalQuadrupleExtraction, calculate_first, calculate_follow, \
    construct_parsing_table


class ParsingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Predictive Parser")

        self.setup_ui()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both")

        self.setup_input_frame()
        self.setup_output_frames()

    def setup_input_frame(self):
        self.input_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.input_frame, text="Input")

        self.grammar_label = ttk.Label(self.input_frame, text="Grammar:", font=("SimSun", 14))
        self.grammar_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

        self.grammar_text = tk.Text(self.input_frame, height=10, width=70, font=("SimSun", 12))
        self.grammar_text.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        self.grammar_text.insert(tk.END, ("E ::= E + T | T\n"
                                          "T ::= T * F | F\n"
                                          "F ::= ( E ) | i\n"))

        self.input_label = ttk.Label(self.input_frame, text="Input String:", font=("SimSun", 14))
        self.input_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.input_entry = ttk.Entry(self.input_frame, width=50, font=("SimSun", 12))
        self.input_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        self.input_entry.insert(0, "(i+i)*i")

        self.parse_button = ttk.Button(self.input_frame, text="Parse", command=self.parse)
        self.parse_button.grid(row=4, column=0, padx=10, pady=(5, 10), sticky="w")

    def setup_output_frames(self):
        self.left_recursion_frame = ttk.Frame(self.notebook)
        self.first_set_frame = ttk.Frame(self.notebook)
        self.follow_set_frame = ttk.Frame(self.notebook)
        self.parsing_table_frame = ttk.Frame(self.notebook)
        self.parsing_steps_frame = ttk.Frame(self.notebook)
        self.syntax_tree_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.left_recursion_frame, text="Left Recursion")
        self.notebook.add(self.first_set_frame, text="First Set")
        self.notebook.add(self.follow_set_frame, text="Follow Set")
        self.notebook.add(self.parsing_table_frame, text="Parsing Table")
        self.notebook.add(self.parsing_steps_frame, text="Parsing Steps")
        self.notebook.add(self.syntax_tree_frame, text="Syntax Tree")

        # Define font style
        font_style = ("SimSun", 12)
        font_style2 = ("SimSun", 16)

        self.left_recursion_text = tk.Text(self.left_recursion_frame, height=20, width=70, font=font_style2)
        self.left_recursion_text.pack(expand=1, fill="both")

        self.first_set_text = tk.Text(self.first_set_frame, height=20, width=70, font=font_style2)
        self.first_set_text.pack(expand=1, fill="both")

        self.follow_set_text = tk.Text(self.follow_set_frame, height=20, width=70, font=font_style2)
        self.follow_set_text.pack(expand=1, fill="both")

        self.parsing_table_text = tk.Text(self.parsing_table_frame, height=20, width=70, font=font_style2)
        self.parsing_table_text.pack(expand=1, fill="both")

        self.parsing_steps_text = tk.Text(self.parsing_steps_frame, height=20, width=70, font=font_style)
        self.parsing_steps_text.pack(expand=1, fill="both")

        self.tree_canvas = tk.Canvas(self.syntax_tree_frame, width=600, height=400, bg="white")
        self.tree_canvas.pack(expand=1, fill="both")

    def parse(self):
        grammar_string = self.grammar_text.get("1.0", tk.END).strip()
        input_string = self.input_entry.get().strip()

        extractor = GrammaticalQuadrupleExtraction()
        non_terminators, terminators, production, start = extractor.extract_grammar_components(grammar_string)

        non_terminators = ['E', 'T', 'F', "E'", "T'"]
        mid_production = {
            'E': [['T', "E'"]],
            'T': [['F', "T'"]],
            'F': [['i'], ['(', "E", ")"]],
            "E'": [['ε'], ['+', "T", "E'"]],
            "T'": [['ε'], ['*', "F", "T'"]]
        }

        # mid_production = auto_eliminate_left_recursion(production)
        # non_terminators = mid_production.keys()

        first = calculate_first(terminators, non_terminators, mid_production)
        follow = calculate_follow(start, terminators, non_terminators, mid_production, first)
        parsing_table = construct_parsing_table(terminators, non_terminators, mid_production, first, follow)

        parser = PredictiveParser(parsing_table, start)
        result = parser.parse(input_string)

        self.update_output(non_terminators, mid_production, first, follow, parsing_table, parser, result)

    def update_output(self, non_terminators, mid_production, first, follow, parsing_table, parser, result):
        self.left_recursion_text.delete("1.0", tk.END)
        self.first_set_text.delete("1.0", tk.END)
        self.follow_set_text.delete("1.0", tk.END)
        self.parsing_table_text.delete("1.0", tk.END)
        self.parsing_steps_text.delete("1.0", tk.END)

        self.left_recursion_text.insert(tk.END, "消除左递归：\n")
        for nt in non_terminators:
            self.left_recursion_text.insert(tk.END,
                                            f"{nt} -> {' | '.join([' '.join(prod) for prod in mid_production[nt]])}\n")

        self.first_set_text.insert(tk.END, "First 集合:\n")
        for symbol, first_set in first.items():
            self.first_set_text.insert(tk.END, f"{symbol}: {first_set}\n")

        self.follow_set_text.insert(tk.END, "Follow 集合:\n")
        for symbol, follow_set in follow.items():
            self.follow_set_text.insert(tk.END, f"{symbol}: {follow_set}\n")

        self.parsing_table_text.insert(tk.END, "预测分析表:\n")
        self.parsing_table_text.insert(tk.END, "{:<10} {:<10} {:<10}\n".format("非终结符", "终结符", "产生式"))
        for non_terminal, terminals in parsing_table.items():
            for terminal, rules in terminals.items():
                if rules:
                    self.parsing_table_text.insert(tk.END,
                                                   "{:<12} {:<12} {:<10}\n".format(str(non_terminal), str(terminal),
                                                                                   ''.join(rules[0])))

        self.parsing_steps_text.insert(tk.END, "预测分析过程:\n")
        self.parsing_steps_text.insert(tk.END, parser.parsing_steps)

        parser.draw_syntax_tree("syntax_tree.png")
        self.display_tree_image("syntax_tree.png")

    # def display_tree_image(self, image_path):
    #     self.tree_image = Image.open(image_path)
    #     self.tree_photo = ImageTk.PhotoImage(self.tree_image)
    #     self.tree_canvas.create_image(0, 0, anchor=tk.NW, image=self.tree_photo)

    def display_tree_image(self, image_path):
        self.tree_image = Image.open(image_path)
        self.tree_photo = ImageTk.PhotoImage(self.tree_image)
        self.tree_canvas.create_image(0, 0, anchor=tk.NW, image=self.tree_photo)

        # Bind the <Configure> event of the canvas to a method
        self.tree_canvas.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        # Get the size of the canvas
        canvas_width = event.width
        canvas_height = event.height

        # Resize the image to fit the canvas
        resized_image = self.tree_image.resize((canvas_width, canvas_height))
        self.tree_photo = ImageTk.PhotoImage(resized_image)

        # Update the image displayed in the canvas
        self.tree_canvas.create_image(0, 0, anchor=tk.NW, image=self.tree_photo)


if __name__ == "__main__":
    print(banner_str)
    print(banner_str_welcome)
    root = tk.Tk()
    app = ParsingApp(root)
    root.mainloop()
