import tkinter as tk
from tkinter import messagebox

#TODO: Build App with tkinter base on this source

class BasicTkinterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Basic Tkinter App")
        self.root.geometry("300x200")  # Set window size

        # Label
        self.label = tk.Label(root, text="Enter your name:")
        self.label.pack(pady=10)

        # Entry widget
        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)

        # Button
        self.button = tk.Button(root, text="Say Hello", command=self.on_button_click)
        self.button.pack(pady=20)

    # Method to handle button click
    def on_button_click(self):
        user_input = self.entry.get()
        if user_input:
            messagebox.showinfo("Greetings", f"Hello, {user_input}!")
        else:
            messagebox.showwarning("Input Required", "Please enter your name.")
