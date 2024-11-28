import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition



class FaceRecApp:
    def __init__(self, root):
        self.known_encodings = [] #Temporary list. Represents 'database' of known face encodings
        self.known_names = [] #List of known names
        self._root = root
        self._root.title("Face Recognition App")

        self._video = cv2.VideoCapture(0)

        self._video_label = tk.Label(root, anchor='e')
        self._video_label.pack()

        

        self.update_vid()
    
    def update_vid(self):
        ret, frame = self._video.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            #Normalize the frame
            norm_frame = cv2.normalize(rgb_frame, None, 0, 255, cv2.NORM_MINMAX) 
            #Remove noise
            denoised_frame = cv2.GaussianBlur(norm_frame, (5, 5), 0) 

            resized_img = cv2.resize(denoised_frame, (0, 0), fx=0.25, fy=0.25)

            # a list of box coordinates, [(top, right, bottom, left), ...]
            face_locations = face_recognition.face_locations(resized_img, model="hog") 
            face_encodings = face_recognition.face_encodings(resized_img, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                #Scale back up to original size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
                name = "Unknown"
                if True in matches: 
                    first_match_index = matches.index(True) 
                    name = self.known_names[first_match_index]

                cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 3) #Draws a rectangle around the face

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            self._video_label.imgtk = img_tk
            self._video_label.configure(image=img_tk)
        
        self._root.after(10, self.update_vid)
        pass


if __name__=="__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    app = FaceRecApp(root)
    root.mainloop()
