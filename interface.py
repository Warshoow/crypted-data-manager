import tkinter as tk
from tkinter import filedialog
import os

# Créez une classe pour l'interface utilisateur
class AppInterface:
    def __init__(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.file_listbox = None
        self.encrypted_listbox = None


    def button(self, text, command):
        select_button = tk.Button(self.root, text=text, command=command)
        select_button.pack()

    def listbox(self, selectmode = tk.MULTIPLE):
        self.file_listbox = tk.Listbox(self.root, selectmode= selectmode)
        self.file_listbox.pack(side='left')

        self.encrypted_listbox = tk.Listbox(self.root, selectmode=selectmode)
        self.encrypted_listbox.pack(side='right')

    def select_files(self, files_list):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            files_list.extend(file_paths)
            self.update_file_listbox(self.file_listbox, files_list)

    def update_file_listbox(self, listbox, selected_files):
        for file_path in selected_files:
            listbox.insert(tk.END, os.path.basename(file_path))
    
    def delete_file_listbox(self, listbox):
        listbox.delete(0, tk.END)

    def run(self):
        self.root.mainloop()