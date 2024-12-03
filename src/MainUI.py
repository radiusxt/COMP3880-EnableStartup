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
        self.known_encodings = [] #List of known face encodings
        self.known_names = [] #List of known names

        self._settings_window = None
        self._add_user_window = None
        self._delete_user_window = None

        #The main window for the application
        self._root = root
        self._root.title("Face Recognition App")
        self._root.geometry("1920x1080")
        

        self._video = cv2.VideoCapture(0)

        #The main frame in the GUI which holds the video and information frames
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both")

        #Frame for video display
        video_frame = tk.Frame(main_frame)
        video_frame.pack(side="left")

        #Frame for person information
        info_frame = tk.Frame(main_frame)
        info_frame.pack(side="right", padx=10, pady=10)

        #Label to display the video feed along with the box around the persons face
        self._video_label = tk.Label(video_frame, anchor='w')
        self._video_label.pack(side="right", padx=5, pady=5)

        #Label to display the name of the person
        """self._name_label = tk.Label(video_frame, text="Name: ______", font=('Arial', 14), anchor='s')
        self._name_label.pack(fill="x", pady=5, side="bottom")"""

        """self._age_label = tk.Label(info_frame, text="Age: _____", font=('Arial', 14), anchor='w')
        self._age_label.pack(fill="x", pady=5)

        
        self._position_label = tk.Label(info_frame, text="Position: _____", font=('Arial', 14), anchor='w')
        self._position_label.pack(pady=5, side="left")"""

        #Button to open the settings window
        self._settings_button = tk.Button(video_frame, text="Settings", command=self.settings_command)
        self._settings_button.pack(anchor="nw", side="left")

        #Button to close the root window
        self._close_button = tk.Button(video_frame, text="Close", command=self._root.destroy)
        self._close_button.pack(anchor="nw", side="left")

        self._i = True
        self.process_frame = True
        

        self.update_vid()
    
    def update_vid(self):
        ret, frame = self._video.read()
        if ret:
            #Lines 66-77 are just for testing if it can identify my face
            #Later we will have an existing database of face encodings and names.
            #i = True
            if self._i and len(self.known_encodings) < 1:


                test_image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #test_locations = face_recognition.face_locations(test_image_rgb)

                test_encoding = face_recognition.face_encodings(test_image_rgb)
                if len(test_encoding) > 0:
                    self.known_encodings.append(test_encoding[0])
                    self.known_names.append("Sahil")
                    self._i = False

            #Preprocess the frame, detect and attempt to recognise the person in frame
            #Display the name in the name label if person is recognised
            face_detector = FaceDetector(frame)
            if self.process_frame:
                preprocessed_frame = face_detector.preprocess_frame(frame)
                name = face_detector.detect_face(preprocessed_frame, self.known_names, self.known_encodings)
                #self._name_label.config(text=f"Name: {name}")
            self.process_frame = not self.process_frame

            #Update video label to display the current frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)
            img = Image.fromarray(frame_resized)
            img_tk = ImageTk.PhotoImage(image=img)
            self._video_label.imgtk = img_tk
            self._video_label.configure(image=img_tk)
        
        #Update the video label every 10 milliseconds
        self._root.after(10, self.update_vid)

    def settings_command(self):
        #If the settings window is not already open, open it
        if not self._settings_window:
            self._settings_window = True

            #Create a new window to display settings
            self._new_window = tk.Tk()
            self._new_window.title("Settings")
            self._new_window.geometry("1920x1080")

            settings_frame = tk.Frame(self._new_window)
            settings_frame.pack(fill="both", expand=True)

            #Frame for adding users section
            add_frame = tk.Frame(settings_frame)
            add_frame.pack(side="left", padx=10, pady=10)

            #Frame for deleting users section
            delete_frame = tk.Frame(settings_frame)
            delete_frame.pack(side="right", padx=10, pady=10)

            #All widgets required for adding a user
            add_label = tk.Label(add_frame, text="Add User", font=('Arial', 14), anchor="n")
            add_label.pack(side="top", pady=5)

            add_name_frame = tk.Frame(add_frame)
            add_name_frame.pack(side="left")

            add_name_label = tk.Label(add_name_frame, text="Name: ", font=('Arial', 10))
            add_name_label.pack(side="left", pady=5)

            add_name_text = tk.Text(add_name_frame, height=1, width= 15)
            add_name_text.pack(side="left", pady=5)

            #All widgets required for deleting a user
            delete_label = tk.Label(delete_frame, text="Delete User", font=('Arial', 14), anchor="n")
            delete_label.pack(side="top", pady=5)

            delete_name_frame = tk.Frame(delete_frame)
            delete_name_frame.pack(side="left")

            delete_name_label = tk.Label(delete_name_frame, text="Name: ", font=('Arial', 10))
            delete_name_label.pack(side="left", pady=5)

            self.delete_name_text = tk.Text(delete_name_frame, height=1, width= 15)
            self.delete_name_text.pack(side="left", pady=5)

            #Button to close the settings window
            close_settings = tk.Button(self._new_window, text="Close", command=self.close_settings)
            close_settings.pack(pady=20, side="bottom")

            #Button to add a user to the database
            add_user = tk.Button(add_frame, text="Add User")
            add_user.pack(side="bottom", anchor="s", padx=10, pady=5)

            #Button to delete user from the database
            delete_user = tk.Button(delete_frame, text="Delete User", command=self.del_user_command)
            delete_user.pack(side="bottom", anchor="s", padx=10, pady=5)
    
    def close_settings(self) -> None:
        self._settings_window = False
        self._new_window.destroy()

    def add_user_command(self):
        if not self._add_user_window:
            pass

    def del_user_command(self) -> None:
        if not self._delete_user_window:
            #Check if user exists
            user_to_delete = self.delete_name_text.get(1.0, "end-1c")

            if user_to_delete in self.known_names:
                confirm_delete = messagebox.askyesno(title=None, message="Are you sure you "
                                                    "want to remove this user from the database?")
                user_index = self.known_names.index(user_to_delete)

                if confirm_delete:
                    #Remove the name and face encoding from the list of known names and encodings
                    self.known_names.pop(user_index)
                    self.known_encodings.pop(user_index)

                    #Remove the file of the user they entered
                    file_name = self.get_file_name(user_to_delete)
                    file_path = f"../data/{file_name}"
                    os.remove(file_path)

                    #Close the settings window and inform user that deletion was successful.
                    self.close_settings()
                    messagebox.showinfo(title=None, message=f"Successfully deleted user '{user_to_delete}' from Database")
            else:
                #If person is not in the Database, inform the user and close the settings window
                user_not_found = messagebox.showerror(title=None, message="User not found!")
                self.close_settings()

    def get_file_name(self, name: str) -> str:
        file_name = name + ".jpg"
        return file_name

if __name__=="__main__":
    root = tk.Tk()
    #root.geometry("1280x720")
    app = FaceRecApp(root)
    root.mainloop()