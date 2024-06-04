import tkinter as tk

class MyApplication:
    def __init__(self, master):
        self.master = master
        master.title("Dropdown Menu Example")

        self.dropdown_var = tk.StringVar(master)
        self.dropdown_var.set("Option 1")  # Default option

        self.dropdown = tk.OptionMenu(master, self.dropdown_var, "Option 1", "Option 2", "Option 3")
        self.dropdown.pack()

        self.button = tk.Button(master, text="Print Selection", command=self.print_selection)
        self.button.pack()

    def print_selection(self):
        selected_option = self.dropdown_var.get()
        print("Selected option:", selected_option)

root = tk.Tk()
app = MyApplication(root)
root.mainloop()
