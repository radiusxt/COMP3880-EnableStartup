import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from AddUserUI import AddUserUI


class SettingsUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_user_window = False
        self.add_user_ui = None

        self.title("Settings")
        self.geometry("1200x600")
        self.configure(bg="#3c3d3c")

        self.scroll_pending = False

        self.parent = parent
        self.settings_rows = []
        self.data = []
        self.known_names = []
        self.known_encodings = []

        self.populate_initial_faces()

        buttons_frame = tk.Frame(self, bg="#3c3d3c")
        buttons_frame.pack(fill="x", side="top")

        frame = tk.Frame(self, bg="#3c3d3c")
        frame.pack(expand=True, fill="both")

        container = tk.Frame(frame, bg="#3c3d3c")
        container.pack(expand=True, fill="both", pady=10)

        self.canvas = tk.Canvas(container, bg="#3c3d3c", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=10)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="left", fill="y")

        self.table_frame = tk.Frame(self.canvas, bg="#3c3d3c")
        self.table_frame_id = self.canvas.create_window((0, 0), window=self.table_frame, anchor="n")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.table_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<Configure>", self.update_scroll_region)

        self.create_settings_table()

        # Button to close the settings window
        close_settings = tk.Button(buttons_frame, text="Close", fg="white", bg="#001314", command=self.close_settings, width=15, font=("Arial", 10, "bold"))
        close_settings.pack(side="left", anchor="n", padx=75, pady=25)

        add_user_button = tk.Button(buttons_frame, text="Add User", fg="white", bg="#001314", width=15, font=("Arial", 10, "bold"), command=self.add_user_cmd)
        add_user_button.pack(side="right", anchor="n", padx=75, pady=25)
    
    def update_scroll_region(self, event=None):
        self.scroll_pending = False
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        canvas_width = self.canvas.winfo_width()
        table_width = self.table_frame.winfo_width()
        x_offset = max((canvas_width - table_width) // 2, 0)
        self.canvas.coords(self.table_frame_id, x_offset, 0)
    
    def create_settings_table(self):
        headers = ["Name", "File Path", "Action"]

        for i, header in enumerate(headers):
            label = tk.Label(self.table_frame, text=header, fg="white", bg="#001314", font=("Arial", 16, "bold"), width=15, anchor="center")
            label.grid(row=0, column=i, pady=5, padx=1, sticky="nsew")
            self.table_frame.columnconfigure(i, weight=1)
        
        for i, (c1, c2) in enumerate(self.data):
            self.add_row(i+1, c1, c2, self.table_frame)
        
    def add_row(self, row, text_col1, text_col2, frame):
        col1 = tk.Label(frame, text=text_col1, fg="white", bg="#3c3d3c", font=("Arial", 16), anchor='w')
        col2 = tk.Label(frame, text=text_col2, fg="white", bg="#3c3d3c", font=("Arial", 16), anchor='w')
        col3 = tk.Button(frame, text="X", fg="red", bg="#001314", font=("Arial", 16, "bold"), command=lambda r=row: self.delete_row(r))

        col1.grid(row=row, column=0, pady=2, padx=1, sticky="nsew")
        col2.grid(row=row, column=1, pady=2, padx=1, sticky="nsew")
        col3.grid(row=row, column=2, pady=2, padx=1, sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)
        frame.columnconfigure(2, weight=0)

        self.settings_rows.append((col1, col2, col3))
    
    def delete_row(self, row):
        name = ""
        file_path = ""

        confirm_delete = messagebox.askyesno(parent=self, title=None,
                        message="Are you sure you want to remove this user from the database?")

        if confirm_delete:
            # Remove the name and face encoding from the list of known names and encodings
            
            for i, widget in enumerate(self.settings_rows[row - 1]):
                if i == 0:
                    name = widget.cget("text")
                elif i == 1:
                    file_path = widget.cget("text")
                widget.destroy()

            self.settings_rows[row - 1] = (None, None, None)

            data_index = self.data.index((name, file_path))
            self.data.pop(data_index)

            user_index = self.known_names.index(name)
            self.known_names.pop(user_index)
            #self.known_encodings.pop(user_index)

            os.remove(file_path)

            messagebox.showinfo(parent=self, title=None, message=f"Successfully deleted user '{name}' from Database")
        #return self.known_names, self.known_encodings
        return self.known_names
    
    def close_settings(self) -> None:
        """Closes the settings window. Called when the close button is pressed in settings."""

        self.parent._settings_window = False
        self.settings_rows = []
        self.destroy()
        self.parent.deiconify()

    def add_user_cmd(self) -> None:
        if not self.add_user_window:
            self.add_user_window = True
            self.add_user_ui = AddUserUI(self, self.parent)

    def populate_initial_faces(self) -> None:
        """
        Populates known names and known encodings list with users that are already in the
        database.
        """
        directory = "./faces"

        # For each user, generate the encoding and extract the name, then append these to
        # the respective lists
        for name in os.listdir(directory):
            file_path = f"./faces/{name}"
            file_name_split = name.split('.')
            user_name = file_name_split[0]
            self.known_names.append(user_name)
            self.data.append((user_name, file_path))
        