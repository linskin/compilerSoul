import tkinter as tk
from tkinter import scrolledtext

from compress_grammar import GrammarCleaner
from extract_grammar import GrammaticalQuadrupleExtraction
from print_productions import print_productions

s = "E ::= E + T | T \nT ::= T * F | F \nF ::= ( E ) | i"


class MyOutputWindow:
    def __init__(self, grammar_string=s, master=tk.Tk()):
        self._print_cleaned_production = None
        self._cleaned_production = None
        self._cleaner = None
        self._start = None
        self._production = None
        self._non_terminators = None
        self._terminators = None
        self._extractor = None
        self._grammar_string = grammar_string
        self.__information_init()

        # Create main window
        self._root = master
        self._root.title("Output Window")
        self._root.configure(bg="#f0f0f0")
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        self._root.geometry(f"+{(screen_width - 400) // 2}+{(screen_height - 270) // 2}")
        self._root.resizable(False, False)

        # Frame to hold content
        self._content_frame = tk.Frame(self._root, bg="#f0f0f0")
        self._content_frame.pack(padx=10, pady=10)

        # Output text area
        self._output_text_area = scrolledtext.ScrolledText(self._content_frame, width=40, height=10, bg='#ffffff',
                                                           wrap=tk.WORD, font=("Courier", 12))
        self._output_text_area.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.__update_output_text("Welcome!")
        # self._output_text_area.config(state=tk.DISABLED)

        # Button to close the window
        self._close_button = tk.Button(self._content_frame, text="Close", command=self._root.destroy, bg='#d32f2f',
                                       fg='white', font=("Courier", 12, "bold"))
        self._close_button.grid(row=1, column=3, padx=20, pady=10, sticky="nsew")

        # Create page buttons
        self.page1_button = tk.Button(self._content_frame, text="Grammar", command=self.__show_page1)
        self.page1_button.grid(row=1, column=0, padx=0, pady=10, sticky="nsew")

        self.page2_button = tk.Button(self._content_frame, text="GrammaticalExtraction", command=self.__show_page2)
        self.page2_button.grid(row=1, column=1, padx=0, pady=10, sticky="nsew")

        self.page3_button = tk.Button(self._content_frame, text="CompressGrammar", command=self.__show_page3)
        self.page3_button.grid(row=1, column=2, padx=0, pady=10, sticky="nsew")

        # self.page4_button = tk.Button(self._content_frame, text="CompressGrammar", command=self.__show_page4)
        # self.page4_button.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")

        # self.dropdown_var = tk.StringVar(master)
        # self.dropdown_var.set("Option 1")  # Default option

        # self.dropdown = tk.OptionMenu(self._content_frame, self.dropdown_var, "Option 1", "Option 2", "Option 3")
        # self.dropdown.grid(row=2, column=1, padx=0, pady=0, sticky="nsew")
        #
        # self.button = tk.Button(self._content_frame, text="Print Selection", command=self.print_selection)
        # self.button.grid(row=2, column=2, padx=0, pady=0, sticky="nsew")

    # def print_selection(self):
    #     selected_option = self.dropdown_var.get()
    #     print("Selected option:", selected_option)

    def __information_init(self):
        self._extractor = GrammaticalQuadrupleExtraction()
        self._terminators, self._non_terminators, self._production, self._start = \
            (self._extractor.extract_grammar_components(self._grammar_string))
        self._cleaner = GrammarCleaner()
        self._cleaned_production = self._cleaner.auto_clean(self._production, self._start, self._terminators)
        self._print_cleaned_production = print_productions(self._cleaned_production)

    def __update_output_text(self, new_text):
        self._output_text_area.config(state=tk.NORMAL)  # Enable editing
        self._output_text_area.delete("1.0", tk.END)  # Delete current content
        self._output_text_area.insert(tk.END, new_text)  # Insert new content
        self._output_text_area.config(state=tk.DISABLED)  # Disable editing

    def __productions_arrow(self):
        result = ""
        for key in self._production:
            for item in self._production[key]:
                if item == '':
                    continue
                result += "  " + key + " =>+ {" + " ".join(item) + "}\n"
        return result[:-1]

    def __show_page1(self):
        ans = "Grammar string:\n" + self._grammar_string + "\n"
        self.__update_output_text(ans)

    def __show_page2(self):
        ans = ("Vt : " + " ".join(self._terminators) + "\n" +
               "Vn : " + " ".join(self._non_terminators) + "\n" +
               "P : \n" + self.__productions_arrow() + "\n" +
               "S : " + self._start + "\n")
        self.__update_output_text(ans)

    def __show_page3(self):
        ans = "compressed production : \n" + self._print_cleaned_production
        self.__update_output_text(ans)

    # def __show_page4(self):
    #     ans = ""
    #     self.__update_output_text(ans)

    def run(self):
        self._root.mainloop()


if __name__ == '__main__':
    output = """
        Vt :  + * ( ) i\n
        Vn :  E T F\n
        P :  E ::= E + T | T\n
             T ::= T * F | F\n
             F ::= ( E ) | i\n
             S :  E\n
        cleaned production :\n 
        E -> E + T | T\n
        T -> T * F | F\n
        F -> ( E ) | i\n
        """
    # 实例化一个窗口类并运行
    mow_win = MyOutputWindow()
    mow_win.run()
