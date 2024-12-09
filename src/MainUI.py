import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
import os
import sys
sys.path.append("/home/pi/.local/pipx/venvs/face-recognition/lib/python3.11/site-packages")
import face_recognition
import threading
import time
from modules.face_detector import FaceDetector
from modules.face_identifier import FaceIdentifier

cv2.ocl.setUseOpenCL(True)

class FaceRecApp:
    def __init__(self, root: tk.Tk):
        # List of known face encodings
        self.known_encodings = []

        # List of known names
        self.known_names = [] 

        self.populate_initial_faces()

        self.face_detector = FaceDetector()
        self.face_identifier = FaceIdentifier()

        #Variables to keep track of whether the respective windows are open
        self._settings_window = None
        self._add_user_window = None
        self._delete_user_window = None

        #The main window for the application
        self._root = root
        self._root.title("Face Recognition App")
        self._root.geometry("1200x600")

        #The main frame in the GUI which holds the video and information frames
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both")

        #Frame for video display
        video_frame = tk.Frame(main_frame)
        video_frame.pack(side="left")

        #Frame for person information
        info_frame = tk.Frame(main_frame)
        info_frame.pack(side="right", padx=10, pady=10)

        #Label to display detected face
        self._face_label = tk.Label(info_frame, anchor='n', text="No close face detected")
        self._face_label.pack(side="top", padx=5, pady=5)

        #Label to display name of detected face if recognised
        self._name_label = tk.Label(info_frame, text="Name: _____", anchor='n')
        self._name_label.pack(side="top")

        #Frame to store confirm and cancel buttons
        buttons_frame = tk.Frame(info_frame)
        buttons_frame.pack(side="bottom")

        #Button to clear face frame 
        self._cancel_button = tk.Button(buttons_frame, text="Cancel", anchor='s', command=self.confirm_command)
        self._cancel_button.pack(side="right")

        #Button to confirm that detected face and displayed name are correct
        self._confirm_button = tk.Button(buttons_frame, text="Confirm", anchor='s', command=self.confirm_command)
        self._confirm_button.pack(side="right")

        #Label to display the video feed along with the box around the persons face
        self._video_label = tk.Label(video_frame, anchor='w')
        self._video_label.pack(side="right", padx=5, pady=5)

        #Button to open the settings window
        self._settings_button = tk.Button(video_frame, text="Settings", command=self.settings_command)
        self._settings_button.pack(anchor="nw", side="left")

        #Button to close the root window
        self._close_button = tk.Button(video_frame, text="Close", command=self._root.destroy)
        self._close_button.pack(anchor="nw", side="left")

        self.face_detected = False

        #Thread to update video feed
        self.video_thread = threading.Thread(target = self.update_vid)
        self.video_thread.daemon = True
        self.video_thread.start()

        #Thread to update face frame with detected face
        self.face_thread = threading.Thread(target = self.update_face_frame)
        self.face_thread.daemon = True
        self.face_thread.start()

        #Variables to store detected face in image and numpy array formats
        self._detected_face_img = None
        self._face_frame_arr = None

        #self.process_frame = True
        self._frame = None
    
    def update_vid(self) -> None:
        """Updates the video label with the frame read from the webcam."""

        while True:
            frame, _, _, _, _ = self.face_detector.get_frame()
            if frame:
                self._video_label.configure(image=frame)
                self._video_label.image = frame
            
            #Pause for 30 milliseconds before updating to reduce CPU usage.
            time.sleep(0.030)

    def update_face_frame(self) -> None:
        """Updates face label with detected face if there is a face detected."""

        while True:
            full_frame, detected_face_frame, frame, face_locations, face_frame_arr = self.face_detector.get_frame()
            if detected_face_frame and not self.face_detected:
                self._frame = frame
                self._face_label.configure(image=detected_face_frame, text="")
                self._face_label.image = detected_face_frame
                self._detected_face_img = detected_face_frame
                self._face_frame_arr = face_frame_arr
                self.face_detected = True

                # name = self.face_identifier.identify_face(self._detected_face_img, face_locations, self.known_encodings, self.known_names)
                # self._name_label.config(text=f"Name: {name}")
            elif not detected_face_frame and not self.face_detected:
                self._face_label.configure(text="No close face detected")
                self._name_label.configure(text="")
                self._detected_face_img = None
            
            #Pause for 100 milliseconds before updating to reduce CPU usage.
            time.sleep(0.1)

    def settings_command(self):
        """Opens and initialises settings window widgets."""

        #If the settings window is not already open, open it
        if not self._settings_window:
            self._settings_window = True

            #Create a new window to display settings
            self._new_window = tk.Tk()
            self._new_window.title("Settings")
            self._new_window.geometry("1200x600")

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

            self.add_name_text = tk.Text(add_name_frame, height=1, width= 15)
            self.add_name_text.pack(side="left", pady=5)

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
            add_user = tk.Button(add_frame, text="Add User", command=self.add_user_command)
            add_user.pack(side="bottom", anchor="s", padx=10, pady=5)

            #Button to delete user from the database
            delete_user = tk.Button(delete_frame, text="Delete User", command=self.del_user_command)
            delete_user.pack(side="bottom", anchor="s", padx=10, pady=5)
    
    def close_settings(self) -> None:
        """Closes the settings window. Called when the close button is pressed in settings."""

        self._settings_window = False
        self._new_window.destroy()

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
            #messagebox.showinfo(title=None, message="Ensure you are standing in front of the camera")

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
        directory = "./faces"
        for name in os.listdir(directory):
            file_path = f"./faces/{name}"
            img = Image.open(file_path)
            img_arr = np.asarray(img)
            encoding = face_recognition.face_encodings(img_arr)
            if len(encoding) > 0:
                self.known_encodings.append(encoding[0])
            
            file_name_split = name.split('.')
            user_name = file_name_split[0]
            self.known_names.append(user_name)

if __name__=="__main__":
    root = tk.Tk()
    app = FaceRecApp(root)
    root.mainloop()