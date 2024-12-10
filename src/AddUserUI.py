import tkinter as tk
from tkinter import messagebox
import time


class AddUserUI:
    def __init__(self, settings, main):
        if hasattr(self, 'window') and self._add_window.winfo_exists():
            # If window already exists, bring it to focus
            self._add_window.deiconify()
            return
        
        self.settings = settings
        self.main = main

        self.known_names = self.main.known_names
        self.known_encodings = self.main.known_encodings

        self.face_img = None
        self.face_arr = None

        self._add_window = tk.Toplevel(main)
        self._add_window.title("Add User")
        self._add_window.geometry("800x600")
        self._add_window.configure(bg="#3c3d3c")

        self.face_label = tk.Label(self._add_window, text="No Face Detected", fg="white", bg="#3c3d3c", font=("Arial", 16))
        self.face_label.pack(side="top", pady=10, fill="both", expand=True)

        self.name_frame = tk.Frame(self._add_window, height=1, bg="#3c3d3c")
        self.name_frame.pack(side="top", pady=10)

        self.name_label = tk.Label(self.name_frame, text="Name", fg="white", bg="#3c3d3c", font=("Arial", 16), height=1)
        self.name_label.pack(side="left", padx=5)

        self.name_text = tk.Text(self.name_frame, width=20, height=1, font=("Arial", 14))
        self.name_text.pack(side="left", padx=5)

        self.buttons_frame = tk.Frame(self._add_window, bg="#3c3d3c")
        self.buttons_frame.pack(side="top", pady=10)

        self.confirm_button = tk.Button(self.buttons_frame, width=15, text="Confirm")
        self.confirm_button.pack(side="left", padx=10)

        self.cancel_button = tk.Button(self.buttons_frame, width=15, text="Cancel", command=self.cancel_cmd)
        self.cancel_button.pack(side="left", padx=10)

        self.retry_button = tk.Button(self.buttons_frame, text="Retry", width=15, command=self.retry_cmd)
        self.retry_button.pack(side="left", padx=10)

        self.detect_frame()
        if self.face_img:
            self.face_label.configure(image=self.face_img, text="")
            self.face_label.image = self.face_img
    
    def detect_frame(self):
        time.sleep(0.2)
        self.face_label.configure(text="No Face Detected")

        _, detected_face_frame, _, _, face_frame_arr = self.main.face_detector.get_frame()
        if detected_face_frame:
            self.face_img = detected_face_frame
            self.face_arr = face_frame_arr
        else:
            self.face_img = None
            self.face_arr = None
    
    def retry_cmd(self):
        self.detect_frame()
        if self.face_img:
            self.face_label.configure(image=self.face_img, text="")
            self.face_label.image = self.face_img
            return
        
        self.face_label.configure(text="No Face Detected")
        messagebox.showwarning(parent=self._add_window, title=None, message="Face not detected. Press retry to try again")
        return
            
    def cancel_cmd(self):
        self._add_window.destroy()
        self.main.deiconify()
