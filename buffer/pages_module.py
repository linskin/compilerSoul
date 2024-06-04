import tkinter as tk

class MyWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My Application")

        # Create page buttons
        self.page1_button = tk.Button(self.root, text="Page 1", command=self.show_page1)
        self.page1_button.grid(row=0, column=0, padx=10, pady=10)

        self.page2_button = tk.Button(self.root, text="Page 2", command=self.show_page2)
        self.page2_button.grid(row=0, column=1, padx=10, pady=10)

        self.page3_button = tk.Button(self.root, text="Page 3", command=self.show_page3)
        self.page3_button.grid(row=0, column=2, padx=10, pady=10)

        # Create start button
        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.grid(row=1, columnspan=3, padx=10, pady=10)

        # Initialize variables to keep track of current page
        self.current_page = None

    def show_page1(self):
        self.current_page = "Page 1"
        print("Showing Page 1")

    def show_page2(self):
        self.current_page = "Page 2"
        print("Showing Page 2")

    def show_page3(self):
        self.current_page = "Page 3"
        print("Showing Page 3")

    def start(self):
        if self.current_page:
            print("Starting with current page:", self.current_page)
        else:
            print("Please select a page first.")

    def run(self):
        self.root.mainloop()

# Create an instance of the MyWindow class and run the application
window = MyWindow()
window.run()
