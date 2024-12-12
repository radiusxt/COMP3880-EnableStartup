import cv2
import numpy as np
import sys
sys.path.append("/home/pi/.local/pipx/venvs/face-recognition/lib/python3.11/site-packages")
import face_recognition
import json


class FaceIdentifier:
    def __init__(self):
        self.data = None
    
    def identify_face(self, frame):
        with open("data.json", 'r') as file:
            self.data = json.load(file)
        name = ""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            encoding = face_recognition.face_encodings(rgb_frame)[0]
        except:
            return ""
        cosine_similarities = []
        if len(encoding) > 0 and len(self.data) > 0:
            for entry in self.data:
                known_encoding = entry["encoding"]
                cosine_similarities.append(np.dot(encoding, known_encoding) / (np.linalg.norm(encoding) * np.linalg.norm(known_encoding))) 
            best_match_index = np.argmax(cosine_similarities)
            if cosine_similarities[best_match_index] > 0.95:
                name = self.data[best_match_index]["name"]
        return name
