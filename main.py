import numpy
import cv2
import face_recognition


#image = face_recognition.load_image_file("DSC04401.JPG")
video_capture = cv2.VideoCapture(0)

known_encodings = [] #Temporary list. Represents 'database' of known face encodings
known_names = [] #List of known names

while True:
    ret, frame = video_capture.read()
    #Convert BGR to RGB as face_recognition requires RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    #Normalize the frame
    norm_frame = cv2.normalize(rgb_frame, None, 0, 255, cv2.NORM_MINMAX) 
    #Remove noise
    denoised_frame = cv2.GaussianBlur(norm_frame, (5, 5), 0) 

    # a list of box coordinates, [(top, right, bottom, left), ...]
    face_locations = face_recognition.face_locations(denoised_frame, model="cnn") 
    face_encodings = face_recognition.face_encodings(denoised_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"
        if True in matches: 
            first_match_index = matches.index(True) 
            name = known_names[first_match_index]

        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 3) #Draws a rectangle around the face

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): #Quits the program when q is pressed
        break


video_capture.release()
cv2.destroyAllWindows()

# Convert to BGR for OpenCV (optional, as OpenCV uses BGR format)
#image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# Draw rectangles around faces


# Display the result
#cv2.imshow("Image", image)
#cv2.waitKey(0)
#video_capture.release()
#cv2.destroyAllWindows()