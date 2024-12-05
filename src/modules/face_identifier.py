# TODO: implement Face Identifier
import face_recognition

class FaceIdentifier:
    def __init__(self):
        pass

    def identify_face(self, frame, location, known_encodings, known_names):
        encoding = face_recognition.face_encodings(frame, location)
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
        return name