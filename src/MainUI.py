import tkinter as tk
import cv2
from PIL import Image, ImageTk
import sys
sys.path.append("/home/pi/.local/pipx/venvs/face-recognition/lib/python3.11/site-packages")
import face_recognition
from modules.face_detector import FaceDetector

class FaceRecApp:
    def __init__(self, root: tk.Tk):
        self.known_encodings = [] #Temporary list. Represents 'database' of known face encodings
        self.known_names = [] #List of known names

        self._root = root
        self._root.title("Face Recognition App")
        self._root.geometry("1920x1080")

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
        
        self._root.after(10, self.update_vid)
        pass


if __name__=="__main__":
    root = tk.Tk()
    #root.geometry("1280x720")
    app = FaceRecApp(root)
    root.mainloop()
