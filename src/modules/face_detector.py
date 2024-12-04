import cv2
import sys
sys.path.append("/home/pi/.local/pipx/venvs/face-recognition/lib/python3.11/site-packages")
import face_recognition

cv2.ocl.setUseOpenCL(True)

class FaceDetector:
    def __init__(self, frame):
        self._frame = frame

    def preprocess_frame(self, frame):
        # Convert BGR to RGB as face_recognition requires RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Normalize the frame
        norm_frame = cv2.normalize(rgb_frame, None, 0, 255, cv2.NORM_MINMAX) 

        # Reduce resolution by 75% for faster processing
        downscaled_frame = cv2.resize(norm_frame, (0, 0), fx=0.25, fy=0.25)
        return downscaled_frame

    @staticmethod
    def match_face(task):
        """Matches a face encoding to known encodings."""
        face_encoding, known_encodings, known_names = task
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
        return name
    
    def detect_face(self, frame, known_names, known_encodings, pool):
        name = "Unknown"

        # List of box coordinates, [(top, right, bottom, left), ...]
        face_locations = face_recognition.face_locations(frame, model="hog") 
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Prepare tasks for multiprocessing
        tasks = [(encoding, known_encodings, known_names) for encoding in face_encodings]

        # Process face matching in parallel
        results = pool.map(self.match_face, tasks)

        """for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Scale back to original size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            
            if True in matches: 
                first_match_index = matches.index(True) 
                name = known_names[first_match_index]

            # Draws a rectangle around the face
            cv2.rectangle(self._frame, (left, top), (right, bottom), (255, 255, 0), 3)

            cv2.rectangle(self._frame, (left, bottom + 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self._frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        """
        for (top, right, bottom, left), name in zip(face_locations, results):
            # Scale back to the original frame size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle around the face
            cv2.rectangle(self._frame, (left, top), (right, bottom), (255, 255, 0), 3)

            # Label the face
            cv2.rectangle(self._frame, (left, bottom + 35), (right, bottom), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self._frame, name, (left + 5, bottom + 25), font, 1.0, (255, 255, 255), 1)
        
        return name