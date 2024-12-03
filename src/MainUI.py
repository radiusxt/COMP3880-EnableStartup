import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import os
import sys
sys.path.append("/home/pi/.local/pipx/venvs/face-recognition/lib/python3.11/site-packages")
import face_recognition
from modules.face_detector import FaceDetector

cv2.ocl.setUseOpenCL(True)

class FaceRecApp:
    def __init__(self, root: tk.Tk):
        self.known_encodings = [] #Temporary list. Represents 'database' of known face encodings
        self.known_names = [] #List of known names

        self._settings_window = None
        self._add_user_window = None
        self._delete_user_window = None

        self._root = root
        self._root.title("Face Recognition App")
        self._root.geometry("640x480")

        self._video = cv2.VideoCapture(0)

        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        #Frame for video display
        video_frame = tk.Frame(main_frame)
        video_frame.pack(side="left", padx=10, pady=10)

        #Frame for person information
        info_frame = tk.Frame(main_frame)
        info_frame.pack(side="right", padx=10, pady=10)


        self._video_label = tk.Label(video_frame, anchor='e')
        self._video_label.pack(side="left", padx=25, pady=25)

        self._name_label = tk.Label(info_frame, text="Name: ______", font=('Arial', 14), anchor='w')
        self._name_label.pack(fill="x", pady=5)

        self._age_label = tk.Label(info_frame, text="Age: _____", font=('Arial', 14), anchor='w')
        self._age_label.pack(fill="x", pady=5)

        self._position_label = tk.Label(info_frame, text="Position: _____", font=('Arial', 14), anchor='w')
        self._position_label.pack(pady=5, side="left")

        self._settings_button = tk.Button(self._root, text="Settings", command=self.settings_command)
        self._settings_button.pack(pady=10, side="bottom")

        self._close_button = tk.Button(self._root, text="Close", command=self._root.destroy)
        self._close_button.pack(pady=10, side="bottom")

        self.update_vid()
    
    def update_vid(self):
        ret, frame = self._video.read()
        if ret:
            #Lines 51-63 are just for testing if it can identify my face
            #Later we will have an existing database of face encodings and names.
            i = True
            if i and len(self.known_encodings) < 1:


                test_image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                test_locations = face_recognition.face_locations(test_image_rgb)
                print(f"[debug] test_locations: {test_locations}")

                test_encoding = face_recognition.face_encodings(test_image_rgb)
                if len(test_encoding) > 0:
                    self.known_encodings.append(test_encoding[0])
                    self.known_names.append("Sahil")
                    i = False

            face_detector = FaceDetector(frame)
            preprocessed_frame = face_detector.preprocess_frame(frame)
            name = face_detector.detect_face(preprocessed_frame, self.known_names, self.known_encodings)
            self._name_label.config(text=f"Name: {name}")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            self._video_label.imgtk = img_tk
            self._video_label.configure(image=img_tk)
        
        self._root.after(1, self.update_vid)

    def settings_command(self):
        if not self._settings_window:
            self._settings_window = True
            self._new_window = tk.Tk()
            self._new_window.title("Settings")
            self._new_window.geometry("640x480")

            settings_frame = tk.Frame(self._new_window)
            settings_frame.pack(fill="both", expand=True)

            #Frame for video display
            add_frame = tk.Frame(settings_frame)
            add_frame.pack(side="left", padx=10, pady=10)

            #Frame for person information
            delete_frame = tk.Frame(settings_frame)
            delete_frame.pack(side="right", padx=10, pady=10)

            add_label = tk.Label(add_frame, text="Add User", font=('Arial', 14), anchor="n")
            add_label.pack(side="top", pady=5)

            add_name_frame = tk.Frame(add_frame)
            add_name_frame.pack(side="left")

            add_name_label = tk.Label(add_name_frame, text="Name: ", font=('Arial', 10))
            add_name_label.pack(side="left", pady=5)

            add_name_text = tk.Text(add_name_frame, height=1, width= 15)
            add_name_text.pack(side="left", pady=5)

            delete_label = tk.Label(delete_frame, text="Delete User", font=('Arial', 14), anchor="n")
            delete_label.pack(side="top", pady=5)

            delete_name_frame = tk.Frame(delete_frame)
            delete_name_frame.pack(side="left")

            delete_name_label = tk.Label(delete_name_frame, text="Name: ", font=('Arial', 10))
            delete_name_label.pack(side="left", pady=5)

            self.delete_name_text = tk.Text(delete_name_frame, height=1, width= 15)
            self.delete_name_text.pack(side="left", pady=5)

            #self._delete_user_name = delete_name_text.get(1.0, "end-1c")

            close_settings = tk.Button(self._new_window, text="Close", command=self.close_settings)
            close_settings.pack(pady=20, side="bottom")

            add_user = tk.Button(add_frame, text="Add User")
            add_user.pack(side="bottom", anchor="s", padx=10, pady=5)

            delete_user = tk.Button(delete_frame, text="Delete User", command=self.del_user_command)
            delete_user.pack(side="bottom", anchor="s", padx=10, pady=5)
    
    def close_settings(self):
        self._settings_window = False
        self._new_window.destroy()

    def add_user_command(self):
        if not self._add_user_window:
            pass

    def del_user_command(self):
        if not self._delete_user_window:
            #Check if user exists
            user_to_delete = self.delete_name_text.get(1.0, "end-1c")
            if user_to_delete in self.known_names:
                confirm_delete = messagebox.askyesno(title=None, message="Are you sure you "
                                                    "want to remove this user from the database?")
                if confirm_delete:
                    #Remove the file of the user they entered
                    file_name = self.get_file_name(user_to_delete)
                    #print(f"User pressed yes. File name to delete is {file_name}")
                    file_path = f"../data/{file_name}"
                    print(f"[debug] file path is {file_path}")
                    os.remove(file_path)
                    pass
            
            else:
                #print(f"[debug] name: {user_to_delete}")
                #print(f"[debug] known names: {self.known_names}")
                user_not_found = messagebox.showerror(title=None, message="User not found!")

    def get_file_name(self, name: str):
        file_name = name + ".jpg"
        return file_name



if __name__=="__main__":
    root = tk.Tk()
    #root.geometry("1280x720")
    app = FaceRecApp(root)
    root.mainloop()
