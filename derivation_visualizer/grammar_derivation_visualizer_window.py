import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

from print_tree import generate_tree


class GrammarDerivationVisualizer:
    class _InputBox(tk.Entry):
        def __init__(self, master=None, **kwargs):
            super().__init__(master, **kwargs)
            self.var = tk.BooleanVar(master)
            self.bind('<Return>', lambda e: self.var.set(True))

    def __init__(self, production, start_symbol, master=tk.Tk()):
        self._production = production
        self._start_symbol = start_symbol

        # Create main window
        self._root = master
        self._root.title("Grammar Derivation Visualizer")
        self._root.configure(bg="#f0f0f0")
        self._root.resizable(False, False)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        self._root.geometry(f"+{screen_width // 10}+{screen_height // 10}")

        # Input string entry
        self._input_string_label = tk.Label(self._root, text="Target String:", bg="#f0f0f0")
        self._input_string_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self._input_string_entry = tk.Entry(self._root, bg="white", relief="solid", bd=1)
        self._input_string_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Input box for user input
        self._input_label = tk.Label(self._root, text="User Input (press enter):", bg="#f0f0f0")
        self._input_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self._input_box = self._InputBox(self._root, bg="white", relief="solid", bd=1)
        self._input_box.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Output text area
        self._output_label = tk.Label(self._root, text="Output:", bg="#f0f0f0")
        self._output_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self._output_text = scrolledtext.ScrolledText(self._root, width=51, height=14, state=tk.DISABLED,
                                                      relief="solid", bd=1, bg='#ffffff', wrap=tk.WORD,
                                                      font=("Courier", 12))
        self._output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Button to trigger auto derivation
        self._derive_button = tk.Button(self._root, text="Auto Derivation", command=self.__auto_derivation,
                                        bg="#4CAF50", fg="white", relief="raised")
        self._derive_button.grid(row=4, column=0, columnspan=2, pady=5)

    @staticmethod
    def __find_value_in_list(lst, value):
        for i, item in enumerate(lst):
            if item == value:
                return i
        return -1

    def __input_judgment(self):
        inputs = self._input_string_entry.get()
        if inputs == '':
            messagebox.showerror("Error", "Target String cannot be empty!")
            return False
        else:
            return inputs

    def __choose_judgment(self, cnt):
        while True:
            self._root.wait_variable(self._input_box.var)
            answer = self._input_box.get()
            self._input_box.delete(0, tk.END)
            try:
                answer = int(answer)
                if (1 <= answer <= cnt) or answer == -1:
                    return answer
                else:
                    messagebox.showerror("Error", "Please enter a number from 1 to {},"
                                                  " or you can enter -1 to stop.".format(cnt))
                    self._output_text.see(tk.END)  # Scroll to the end of the text
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer")
                self._output_text.see(tk.END)  # Scroll to the end of the text

    def __production_shower(self, production, key):
        self._output_text.insert(tk.END, "Production shower with key {}: \n".format(key))
        for i, item in enumerate(production, start=1):
            mid_str = " ".join(item)
            self._output_text.insert(tk.END, "{}: {} => {}\n".format(i, key, mid_str))
        self._output_text.insert(tk.END, "-1: pull the plug\n")
        self._output_text.insert(tk.END, "-" * 50 + "\n")
        self._output_text.see(tk.END)  # Scroll to the end of the text
        self._output_text.config(state=tk.DISABLED)
        choice = self.__choose_judgment(len(production))
        return choice

    def __result_shower(self, result, tree):
        self._output_text.insert(tk.END, "Derivation process：\n{}\n".format(result))
        ans = generate_tree(tree, self._start_symbol)
        self._output_text.insert(tk.END, "Derivation tree：\n{}\n".format(ans))
        self._output_text.insert(tk.END, "--*--" * 10 + "\n" * 3)
        self._output_text.see(tk.END)  # Scroll to the end of the text
        self._output_text.config(state=tk.DISABLED)

    def __auto_derivation(self):
        input_string = self.__input_judgment()
        if not input_string:
            return
        self._input_string_entry.config(state=tk.DISABLED)
        derived_string = [self._start_symbol]
        result = ""
        tree = {}

        while derived_string:
            derived = False

            for key in self._production:
                if key in derived_string:
                    self._output_text.config(state=tk.NORMAL)  # Enable editing
                    # pos = derived_string.find(key)
                    pos = self.__find_value_in_list(derived_string, key)
                    mid_string = "".join(derived_string)
                    self._output_text.insert(tk.END,
                                             "Deriving {} with key:{} pos:{}\n".format(mid_string, key, pos + 1))

                    choice = self.__production_shower(self._production[key], key)
                    if choice == -1:
                        self._output_text.config(state=tk.NORMAL)
                        self._output_text.insert(tk.END, "You had pull the plug,"
                                                         " the end symbol is {}\n".format(mid_string))
                        # print(tree)
                        self._input_string_entry.config(state=tk.NORMAL)
                        self.__result_shower(result, tree)
                        return
                    end_string = "".join(self._production[key][choice - 1])

                    result += " => {} ({} -> {})\n".format(mid_string, key, end_string)
                    derived_string[pos:pos + 1] = self._production[key][choice - 1]
                    derived = True

                    end_item = [pos + 1, self._production[key][choice - 1]]
                    # 更新语法分析树
                    if key in tree:
                        tree[key].append(end_item)
                    else:
                        tree[key] = [end_item]
                if derived:
                    break

            if ''.join(derived_string) == input_string:
                self._output_text.config(state=tk.NORMAL)
                mid_string_out = "".join(derived_string)
                self._output_text.insert(tk.END, "Derive done, the end symbol is {}\n".format(mid_string_out))
                self.__result_shower(result, tree)
                break
            if not derived:
                self._output_text.config(state=tk.NORMAL)  # Enable editing
                mid_string_out = "".join(derived_string)
                self._output_text.insert(tk.END, "Derive false, the end symbol is {}\n".format(mid_string_out))
                self.__result_shower(result, tree)
                break
        self._input_string_entry.config(state=tk.NORMAL)

    def run(self):
        self._root.mainloop()


if __name__ == '__main__':
    productions2 = {'E': [['E', '+', 'T'], ['T']], 'T': [['T', '*', 'F'], ['F']], 'F': [['(', 'E', ')'], ['i']]}
    productions = {'Ems': [['Ems', '+', 'Tfs'], ['Tfs']], 'Tfs': [['Tfs', '*', "F'"], ["F'"]],
                   "F'": [['(', 'Ems', ')'], ['iss']]}
    start2 = 'E'
    start = 'Ems'

    # 实例化窗口类
    gdv_win = GrammarDerivationVisualizer(productions, start)
    gdv_win.run()
