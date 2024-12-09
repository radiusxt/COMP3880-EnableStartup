# TODO: implement Face Identifier
import face_recognition
import cv2

class FaceIdentifier:
    def __init__(self):
        pass

    def identify_face(self, frame, locations, known_encodings, known_names):
        name = ""
        if len(locations) > 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encoding = face_recognition.face_encodings(frame, locations)
            matches = face_recognition.compare_faces(known_encodings, encoding[0], tolerance=0.6)
            
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
        return name