import tkinter as tk

class MyApplication:
    def __init__(self, master):
        self.master = master
        master.title("Window Position Example")

        # Set the size and position of the window
        window_width = 500
        window_height = 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_position = (screen_width - window_width) // 2  # Center horizontally
        y_position = (screen_height - window_height) // 2  # Center vertically

        master.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.label = tk.Label(master, text="Window position adjusted!")
        self.label.pack()

root = tk.Tk()
app = MyApplication(root)
root.mainloop()
