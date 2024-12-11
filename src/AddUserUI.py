import tkinter as tk
from tkinter import messagebox
import time
import cv2
import sys
sys.path.append("/home/pi/.local/pipx/venvs/face-recognition/lib/python3.11/site-packages")
import face_recognition
from PIL import Image


class AddUserUI(tk.Toplevel):
    def __init__(self, settings, main):
        super().__init__(settings)
        
        self.settings = settings
        self.main = main

        self.face_img = None
        self.face_arr = None

        self.title("Add User")
        self.geometry("800x600")
        self.configure(bg="#3c3d3c")

        self.face_label = tk.Label(self, text="No Face Detected", fg="white", bg="#3c3d3c", font=("Arial", 16))
        self.face_label.pack(side="top", pady=10, fill="both", expand=True)

        self.name_frame = tk.Frame(self, height=1, bg="#3c3d3c")
        self.name_frame.pack(side="top", pady=10)

        self.name_label = tk.Label(self.name_frame, text="Name", fg="white", bg="#3c3d3c", font=("Arial", 16), height=1)
        self.name_label.pack(side="left", padx=5)

        self.name_text = tk.Text(self.name_frame, width=20, height=1, font=("Arial", 14))
        self.name_text.pack(side="left", padx=5)

        self.buttons_frame = tk.Frame(self, bg="#3c3d3c")
        self.buttons_frame.pack(side="top", pady=10)

        self.confirm_button = tk.Button(self.buttons_frame, width=15, text="Confirm", command=self.confirm_cmd)
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
        messagebox.showwarning(parent=self, title=None, message="Face not detected. Press retry to try again")
        return
            
    def cancel_cmd(self):
        self.destroy()
        self.settings.add_user_window = False

    def confirm_cmd(self):
        name = self.name_text.get(1.0, "end-1c")
        if name == "":
            messagebox.showerror(title=None, message="Please enter a name")
            return
        
        if name in self.settings.known_names:
            messagebox.showwarning(title=None, message="User already exists in database!")
            return
        
        rgb_frame = cv2.cvtColor(self.face_arr, cv2.COLOR_BGR2RGB)

        user_encoding = face_recognition.face_encodings(rgb_frame)
        if len(user_encoding) > 0:
            self.settings.known_encodings.append(user_encoding[0])
            self.settings.known_names.append(name)

            file_path = f"./faces/{name}.jpg"
            im = Image.fromarray(rgb_frame)
            im.save(file_path)

            self.settings.data.append((name, file_path))
            self.settings.create_settings_table()

            self.cancel_cmd()

            messagebox.showinfo(title=None, message=f"Successfully added '{name}' to database")
            return
        else:
            messagebox.showwarning(title=None, message="Could not detect any face, please try again!")
            return
