import cv2
import sys
sys.path.append("/home/pi/.local/pipx/venvs/face-recognition/lib/python3.11/site-packages")
import face_recognition
import time
from PIL import Image, ImageTk

cv2.ocl.setUseOpenCL(True)

class FaceDetector:
    def __init__(self):
        # Initialise cv2 video capture
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            raise Exception("Unable to access video feed!")
        
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.min_face_size = 150

        self.face_detected = False
        self.face_frame = None
        self.last_detection_time = 0
        self.face_locations = []

    def preprocess_frame(self, frame):
        rgb_frame = cv2.cvtColor(self.face_frame, cv2.COLOR_BGR2RGB)
        face_img = Image.fromarray(rgb_frame)
        face_tk = ImageTk.PhotoImage(image=face_img)

        return ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))), face_tk
    
    def get_frame(self):
        ret, frame = self.video.read()
        frame = cv2.resize(frame, (640, 480))

        if not ret:
            return None, None, None, None, None
        
        if self.face_detected:
            current_time = time.time()
            
            if current_time - self.last_detection_time > 0:
                self.face_detected = False
                full_frame, face_frame = self.preprocess_frame(frame)
                return (full_frame, face_frame, frame, self.face_locations, self.face_frame)
        
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        faces = self.face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            if w > self.min_face_size and h > self.min_face_size:  # Check if the face is close
                self.face_frame = frame[y:y+h, x:x+w]  # Save the detected face
                self.last_detection_time = time.time()  # Record the time of detection
                self.face_locations.append((y, x + w, y + h, x))
                self.face_detected = True

        return ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))), None, None, self.face_locations, None
    
    def release(self):
        self.video.release()