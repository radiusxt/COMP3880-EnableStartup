import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os


class SettingsUI:
    def __init__(self, parent, settings_rows, known_names, known_encodings, data) -> None:
        if hasattr(self, 'window') and self._new_window.winfo_exists():
            # If window already exists, bring it to focus
            self._new_window.deiconify()
            return
        
        self._new_window = tk.Toplevel(parent)
        self._new_window.title("Settings")
        self._new_window.geometry("1200x600")
        self._new_window.configure(bg="#3c3d3c")

        self.scroll_pending = False

        self.parent = parent
        self.settings_rows = settings_rows
        self.data = data
        self.known_names = known_names
        self.known_encodings = known_encodings

        buttons_frame = tk.Frame(self._new_window, bg="#3c3d3c")
        buttons_frame.pack(fill="x", side="top")

        frame = tk.Frame(self._new_window, bg="#3c3d3c")
        frame.pack(expand=True, fill="both")

        container = tk.Frame(frame, bg="#3c3d3c")
        container.pack(expand=True, fill="both", pady=10)

        canvas = tk.Canvas(container, bg="#3c3d3c", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=10)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="left", fill="y")

        table_frame = tk.Frame(canvas, bg="#3c3d3c")
        self.table_frame_id = canvas.create_window((0, 0), window=table_frame, anchor="n")

        canvas.configure(yscrollcommand=scrollbar.set)

        """def update_scroll_region(self, event=None):
            if self.scroll_pending:
                return
            self.scroll_pending = True
            self.canvas.after(10, self._update_scroll_region)"""

        def update_scroll_region(event=None):
            self.scroll_pending = False
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas_width = canvas.winfo_width()
            table_width = table_frame.winfo_width()
            x_offset = max((canvas_width - table_width) // 2, 0)
            canvas.coords(self.table_frame_id, x_offset, 0)

        table_frame.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", update_scroll_region)

        self.create_settings_table(table_frame)

        # Button to close the settings window
        close_settings = tk.Button(buttons_frame, text="Close", fg="white", bg="#001314", command=self.close_settings, width=15, font=("Arial", 10, "bold"))
        close_settings.pack(side="left", anchor="n", padx=75, pady=25)

        add_user_button = tk.Button(buttons_frame, text="Add User", fg="white", bg="#001314", width=15, font=("Arial", 10, "bold"), command=None)
        add_user_button.pack(side="right", anchor="n", padx=75, pady=25)
    
    def create_settings_table(self, frame):
        headers = ["Name", "File Path", "Action"]

        for i, header in enumerate(headers):
            label = tk.Label(frame, text=header, fg="white", bg="#001314", font=("Arial", 16, "bold"), width=15, anchor="center")
            label.grid(row=0, column=i, pady=5, padx=1, sticky="nsew")
            frame.columnconfigure(i, weight=1)
        
        for i, (c1, c2) in enumerate(self.data):
            self.add_row(i+1, c1, c2, frame)

        return self.settings_rows
        
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

        confirm_delete = messagebox.askyesno(parent=self._new_window, title=None,
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

            messagebox.showinfo(parent=self._new_window, title=None, message=f"Successfully deleted user '{name}' from Database")
        #return self.known_names, self.known_encodings
        return self.known_names
    
    def close_settings(self) -> None:
        """Closes the settings window. Called when the close button is pressed in settings."""

        # self._settings_window = False
        self.parent._settings_window = False
        self.settings_rows = []
        self._new_window.destroy()
        