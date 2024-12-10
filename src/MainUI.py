import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image
import numpy as np
import os
import sys
sys.path.append("/home/pi/.local/pipx/venvs/face-recognition/lib/python3.11/site-packages")
import face_recognition
import threading
import time
from modules.face_detector import FaceDetector
#from modules.face_identifier import FaceIdentifier
from SettingsUI import SettingsUI

cv2.ocl.setUseOpenCL(True)


class FaceRecApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # List of known face encodings and names
        self.known_encodings = []
        self.known_names = [] 

        # List containing tuples of name and file name of users in DB
        self.data = []

        # List containing tuples of widgets in the settings table
        self.settings_rows = []

        self.populate_initial_faces()

        self.face_detector = FaceDetector()
        #self.face_identifier = FaceIdentifier()

        # Variables to keep track of whether the respective windows are open
        self._settings_window = False
        self.settings = None
        self._add_user_window = None
        self._delete_user_window = None

        # The main window for the application
        # self._root = root
        self.title("Face Recognition App")
        self.geometry("1200x600")
        self.configure(bg="#3c3d3c")

        # The main frame in the GUI which holds the video and information frames
        main_frame = tk.Frame(self, bg="#3c3d3c")
        main_frame.pack(fill="both", anchor="center")

        # Frame for video display
        video_frame = tk.Frame(main_frame, bg="#3c3d3c")
        video_frame.pack(side="left")

        # Frame for person information
        info_frame = tk.Frame(main_frame, bg="#3c3d3c")
        info_frame.pack(side="right", padx=10, pady=10)

        buttons_frame = tk.Frame(info_frame, bg="#3c3d3c")
        buttons_frame.pack(side="top")

        # Label to display detected face
        self._face_label = tk.Label(info_frame, anchor='n', text="No close face detected", bg="#3c3d3c", fg="white", font=("Arial", 10, "bold"))
        self._face_label.pack(side="top", padx=50, pady=50)

        # Label to display name of detected face if recognised
        self._name_label = tk.Label(info_frame, text="Name: _____", anchor='n', font=("Arial", 12), fg="white", bg="#3c3d3c")
        self._name_label.pack(side="top", pady=25)

        # Frame to store confirm and cancel buttons
        confirm_frame = tk.Frame(info_frame, bg="#3c3d3c")
        confirm_frame.pack(side="bottom")

        # Button to clear face frame 
        self._cancel_button = tk.Button(confirm_frame, text="Cancel", fg="white", bg="#001314", anchor='s', command=self.confirm_command, width=15, font=("Arial", 10, "bold"))
        self._cancel_button.pack(side="right", padx=25)

        # Button to confirm that detected face and displayed name are correct
        self._confirm_button = tk.Button(confirm_frame, text="Confirm", fg="white", bg="#001314", anchor='s', command=self.confirm_command, width=15, font=("Arial", 10, "bold"))
        self._confirm_button.pack(side="right", padx=25)

        # Button to clear face frame 
        self._quit_button = tk.Button(buttons_frame, text="Quit", fg="white", bg="#001314", anchor='s', command=self.quit_command, width=15, font=("Arial", 10, "bold"))
        self._quit_button.pack(side="right", padx=25)

        # Button to open the settings window
        self._settings_button = tk.Button(buttons_frame, text="Settings", fg="white", bg="#001314", command=self.settings_command, width=15, font=("Arial", 10, "bold"))
        self._settings_button.pack(side="right", padx=25)

        # Label to display the video feed along with the box around the persons face
        self._video_label = tk.Label(video_frame, anchor="center", bg="#3c3d3c")
        self._video_label.pack(padx=5, pady=5)

        self.face_detected = False

        # Thread to update video feed
        self.video_thread = threading.Thread(target = self.update_vid)
        self.video_thread.daemon = True
        self.video_thread.start()

        # Thread to update face frame with detected face
        self.face_thread = threading.Thread(target = self.update_face_frame)
        self.face_thread.daemon = True
        self.face_thread.start()

        # Variables to store detected face in image and numpy array formats
        self._detected_face_img = None
        self._face_frame_arr = None

        self._frame = None
        
    def quit_command(self) -> None:
        """if self._settings_window:
            self._new_window.destroy()"""
        self.destroy()
    
    def update_vid(self) -> None:
        """Updates the video label with the frame read from the webcam."""

        while True:
            # Don't update if settings window is open to improve performance
            if not self._settings_window:
                frame, _, _, _, _ = self.face_detector.get_frame()
                if frame:
                    self._video_label.configure(image=frame)
                    self._video_label.image = frame
                
                # Pause for 30 milliseconds before updating to reduce CPU usage.
                time.sleep(0.030)

    def update_face_frame(self) -> None:
        """Updates face label with detected face if there is a face detected."""

        while True:
            # Don't update if settings window is open to improve performance
            if not self._settings_window:
                full_frame, detected_face_frame, frame, face_locations, face_frame_arr = self.face_detector.get_frame()
                if detected_face_frame and not self.face_detected:
                    self._frame = frame
                    self._face_label.configure(image=detected_face_frame, text="")
                    self._face_label.image = detected_face_frame
                    self._detected_face_img = detected_face_frame
                    self._face_frame_arr = face_frame_arr
                    self.face_detected = True

                    #name = self.face_identifier.identify_face(self._detected_face_img, face_locations, self.known_encodings, self.known_names)
                    #self._name_label.config(text=f"Name: {name}")
                elif not detected_face_frame and not self.face_detected:
                    self._face_label.configure(text="No close face detected")
                    self._name_label.configure(text="Name: ")
                    self._detected_face_img = None
                
                # Pause for 100 milliseconds before updating to reduce CPU usage.
                time.sleep(0.1)

    def settings_command(self):
        """Opens and initialises settings window widgets."""

        # If the settings window is not already open, open it
        if not self._settings_window:
            self._settings_window = True
            self.settings = SettingsUI(self, [], self.known_names, self.known_encodings, self.data)

    def add_user_command(self) -> None:
        """
        Called when the add user button is pressed in the settings menu. Name of user to add
        is collected. If name already exists in the list of known names, a messagebox is displayed
        and the settings menu is closed.

        If the name does not exist in the list of known names, the detected face frame is 
        preprocessed and encoding for this frame is generated. If encoding is properly
        generated, the encoding and name are appended to the list of known encodings
        and known names respectively. The file name is created, the numpy array of
        the detected frame is converted to jpg format, and the frame is stored in the
        faces directory.

        If encoding is not generated, the settings menu is closed and a messagebox is
        displayed to inform the user of the error.
        """
        if not self._add_user_window:
            user_to_add = self.add_name_text.get(1.0, "end-1c")
            if user_to_add in self.known_names:
                self.close_settings()
                messagebox.showwarning(title=None, message="User already exists in database!")
                return
            
            user_image = self._face_frame_arr
            rgb_frame = cv2.cvtColor(user_image, cv2.COLOR_BGR2RGB)
            user_encoding = face_recognition.face_encodings(rgb_frame)
            if len(user_encoding) > 0:
                self.known_encodings.append(user_encoding[0])
                self.known_names.append(user_to_add)

                file_name = self.get_file_name(user_to_add)
                file_path = f"./faces/{file_name}"
                im = Image.fromarray(rgb_frame)
                im.save(file_path)

                self.close_settings()
                messagebox.showinfo(title=None, message=f"Successfully added '{user_to_add}' to database")
                return
            else:
                self.close_settings()
                messagebox.showwarning(title=None, message="Could not detect any face, please try again!")
                return
                
    def del_user_command(self) -> None:
        """
        Called when the delete user button is pressed. Gets the name entered in the name textbox.
        Checks if the name is in the list of known names. If yes, confirm that the user wants to
        delete the person from the database, and remove the user.

        Deleted user's name is removed from the known names list, their encoding is removed from
        the known encodings list, and their face image is removed from the faces directory.

        If the user does not exist in the database, settings menu is closed and messagebox is 
        displayed informing that the user was not found.
        """
        if not self._delete_user_window:
            # Check if a user exists
            user_to_delete = self.delete_name_text.get(1.0, "end-1c")

            if user_to_delete in self.known_names:
                confirm_delete = messagebox.askyesno(title=None,
                        message="Are you sure you want to remove this user from the database?")
                user_index = self.known_names.index(user_to_delete)

                if confirm_delete:
                    # Remove the name and face encoding from the list of known names and encodings
                    self.known_names.pop(user_index)
                    self.known_encodings.pop(user_index)

                    # Remove the file of the user they entered
                    file_name = self.get_file_name(user_to_delete)
                    file_path = f"./faces/{file_name}"
                    os.remove(file_path)

                    # Close the settings window and inform user that deletion was successful
                    self.close_settings()
                    messagebox.showinfo(title=None, message=f"Successfully deleted user '{user_to_delete}' from Database")
                    return
                else:
                    self.close_settings()
                    return
            else:
                # If person is not in the database, inform the user and close the settings window
                self.close_settings()
                messagebox.showerror(title=None, message="User not found!")
                return
                
    def confirm_command(self) -> None:
        """Called when the confirm or cancel buttons are pressed. Resets face label to default text"""

        self.face_detected = False
        self._face_label.configure(image="", text="No close face detected")

    def get_file_name(self, name: str) -> str:
        """
        Creates file name in the required format, which is the name of the user to be stored
        followed by '.jpg'.

        Args:
            name (str): Name of the user
        
        Returns:
            str: The file name in the format "{name}.jpg"
        """
        file_name = name + ".jpg"
        return file_name

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
            img = Image.open(file_path)
            img_arr = np.asarray(img)
            """encoding = face_recognition.face_encodings(img_arr)
            if len(encoding) > 0:
                self.known_encodings.append(encoding[0])"""
            
            file_name_split = name.split('.')
            user_name = file_name_split[0]
            self.known_names.append(user_name)
            self.data.append((user_name, file_path))


if __name__=="__main__":
    # root = tk.Tk()
    app = FaceRecApp()
    app.mainloop()
