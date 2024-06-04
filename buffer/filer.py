import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog


class FileManager:
    def __init__(self, master):
        self.master = master
        self.master.title("File Manager")

        self.current_dir = os.getcwd()
        self.file_listbox = tk.Listbox(master, width=50, height=20)
        self.file_listbox.pack(pady=10)

        self.load_files()

        self.drawer = tk.PanedWindow(master, orient=tk.VERTICAL)
        self.drawer.pack(pady=5)

        self.btn_frame = tk.Frame(self.drawer)
        self.btn_frame.pack(pady=5)

        self.btn_open = tk.Button(self.btn_frame, text="Open", command=self.open_file)
        self.btn_open.pack(side=tk.LEFT, padx=5)

        self.btn_delete = tk.Button(self.btn_frame, text="Delete", command=self.delete_file)
        self.btn_delete.pack(side=tk.LEFT, padx=5)

        self.btn_copy = tk.Button(self.btn_frame, text="Copy", command=self.copy_file)
        self.btn_copy.pack(side=tk.LEFT, padx=5)

        self.btn_move = tk.Button(self.btn_frame, text="Move", command=self.move_file)
        self.btn_move.pack(side=tk.LEFT, padx=5)

        self.btn_refresh = tk.Button(self.btn_frame, text="Refresh", command=self.refresh_files)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)

        self.btn_back = tk.Button(self.btn_frame, text="Back", command=self.go_back)
        self.btn_back.pack(side=tk.LEFT, padx=5)

        self.drawer.add(self.btn_frame)

        self.toggle_drawer_btn = tk.Button(master, text="Toggle Drawer", command=self.toggle_drawer)
        self.toggle_drawer_btn.pack(pady=5)

        self.drawer_expanded = True

    def toggle_drawer(self):
        if self.drawer_expanded:
            self.drawer.pack_forget()
            self.toggle_drawer_btn.config(text="Expand Drawer")
            self.drawer_expanded = False
        else:
            self.drawer.pack(pady=5)
            self.toggle_drawer_btn.config(text="Collapse Drawer")
            self.drawer_expanded = True

    # The rest of the class methods remain unchanged


    def go_back(self):
        self.current_dir = os.path.dirname(self.current_dir)
        self.load_files()

    # The rest of the class methods remain unchanged

    def load_files(self):
        self.file_listbox.delete(0, tk.END)
        for item in os.listdir(self.current_dir):
            self.file_listbox.insert(tk.END, item)

    def open_file(self):
        selected_item = self.file_listbox.curselection()
        if selected_item:
            file_name = self.file_listbox.get(selected_item[0])
            file_path = os.path.join(self.current_dir, file_name)
            if os.path.isdir(file_path):
                self.current_dir = file_path
                self.load_files()
            else:
                os.startfile(file_path)

    def delete_file(self):
        selected_item = self.file_listbox.curselection()
        if selected_item:
            file_name = self.file_listbox.get(selected_item[0])
            file_path = os.path.join(self.current_dir, file_name)
            if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {file_name}?"):
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                self.load_files()

    def copy_file(self):
        selected_item = self.file_listbox.curselection()
        if selected_item:
            file_name = self.file_listbox.get(selected_item[0])
            file_path = os.path.join(self.current_dir, file_name)
            destination = filedialog.askdirectory()
            if destination:
                if os.path.isdir(file_path):
                    shutil.copytree(file_path, os.path.join(destination, file_name))
                else:
                    shutil.copy(file_path, destination)

    def move_file(self):
        selected_item = self.file_listbox.curselection()
        if selected_item:
            file_name = self.file_listbox.get(selected_item[0])
            file_path = os.path.join(self.current_dir, file_name)
            destination = filedialog.askdirectory()
            if destination:
                shutil.move(file_path, os.path.join(destination, file_name))
                self.load_files()

    def refresh_files(self):
        self.load_files()


root = tk.Tk()
app = FileManager(root)
root.mainloop()
