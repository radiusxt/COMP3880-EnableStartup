import tkinter as tk
import cv2
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

        self.face_detector = FaceDetector()
        #self.face_identifier = FaceIdentifier()

        # Variables to keep track of whether the respective windows are open
        self._settings_window = False
        self.settings = None
        self._add_user_window = None
        self._delete_user_window = None

        # The main window for the application
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
        self.detected_face_img = None
        self.face_frame_arr = None

        self.frame = None
        
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
                    self.frame = frame
                    self._face_label.configure(image=detected_face_frame, text="")
                    self._face_label.image = detected_face_frame
                    self.detected_face_img = detected_face_frame
                    self.face_frame_arr = face_frame_arr
                    self.face_detected = True

                    #name = self.face_identifier.identify_face(self._detected_face_img, face_locations, self.known_encodings, self.known_names)
                    #self._name_label.config(text=f"Name: {name}")
                elif not detected_face_frame and not self.face_detected:
                    self._face_label.configure(text="No close face detected")
                    self._name_label.configure(text="Name: ")
                    self.detected_face_img = None
                    self.face_frame_arr = None
                
                # Pause for 100 milliseconds before updating to reduce CPU usage.
                time.sleep(0.1)

    def settings_command(self):
        """Opens and initialises settings window widgets."""

        # If the settings window is not already open, open it
        if not self._settings_window:
            self.withdraw()
            self._settings_window = True
            self.settings = SettingsUI(self)
                
    def confirm_command(self) -> None:
        """Called when the confirm or cancel buttons are pressed. Resets face label to default text"""

        self.face_detected = False
        self._face_label.configure(image="", text="No close face detected")


if __name__=="__main__":
    app = FaceRecApp()
    app.mainloop()
