import cv2
import numpy as np
import torch
import face_recognition
from sklearn.metrics.pairwise import cosine_similarity
from edgeface.backbones import get_model

"""
class FaceIdentifier:
    def __init__(self):
        pass

    def identify_face(self, frame, locations, known_encodings, known_names):
        name = ""
        if len(locations) > 0:
            encoding = face_recognition.face_encodings(frame, locations)
            matches = face_recognition.compare_faces(known_encodings, encoding)
            
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
        return name
"""

class FaceIdentifier:
    def __init__(self):
        # Load the EdgeFace model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = get_model("edgeface_xs_gamma_06")
        self.model.load_state_dict(torch.load(f"edgeface/checkpoints/edgeface_xs_gamma_06.pt", map_location='cpu'))
        self.model.eval()

    def preprocess_face(self, face_image):
        """
        Preprocesses the face image for the EdgeFace model.
        Assumes input is a cropped face.
        """
        # Resize to the model's input size, normalize, and add batch dimension
        face_image = cv2.resize(face_image, (112, 112))  # EdgeFace often uses 112x112 input
        face_image = face_image.astype(np.float32) / 255.0
        face_image = (face_image - 0.5) / 0.5  # Normalize to [-1, 1]
        face_image = np.transpose(face_image, (2, 0, 1))  # Convert to CHW format
        return torch.tensor(face_image, device=self.device).unsqueeze(0)

    def generate_embedding(self, face_image):
        """
        Generates a facial embedding using the EdgeFace model.
        """
        preprocessed = self.preprocess_face(face_image)
        with torch.no_grad():
            embedding = self.model(preprocessed)
        return embedding.cpu().numpy().flatten()

    def identify_face(self, frame, locations, known_encodings, known_names):
        """
        Identifies a face from the detected locations by comparing embeddings.
        
        :param frame: The original image frame.
        :param locations: List of bounding boxes for detected faces.
        :param known_encodings: List of known face embeddings.
        :param known_names: List of names corresponding to the known embeddings.
        :return: The name of the recognized individual or an empty string if no match.
        """
        name = ""
        if len(locations) > 0:
            for location in locations:
                # Extract face from the frame using the bounding box
                top, right, bottom, left = location
                face_image = frame[top:bottom, left:right]

                # Generate embedding for the detected face
                embedding = self.generate_embedding(face_image)

                # Compare with known embeddings using cosine similarity
                similarities = cosine_similarity([embedding], known_encodings)
                best_match_index = np.argmax(similarities)

                if similarities[0, best_match_index] > 0.5:  # Threshold for similarity
                    name = known_names[best_match_index]
        return name