import numpy
import cv2
import sys
sys.path.append("/home/pi/.local/pipx/venvs/face-recognition/lib/python3.11/site-packages")
import face_recognition



#image = face_recognition.load_image_file("DSC04401.JPG")
video_capture = cv2.VideoCapture(0)

"""test_image = face_recognition.load_image_file("DSC04401.JPG")


test_image_rgb = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)

# cv2.imshow("Image", test_image_rgb)
test_locations = face_recognition.face_locations(test_image)
print(f"[debug] test_locations: {test_locations}")

test_encoding = face_recognition.face_encodings(test_image_rgb)[0]"""


known_encodings = [] #Temporary list. Represents 'database' of known face encodings
known_names = [] #List of known names
i = True
while True:
    ret, frame = video_capture.read()
    if i:
        #test_image = face_recognition.load_image_file(frame)


        test_image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # cv2.imshow("Image", test_image_rgb)
        test_locations = face_recognition.face_locations(test_image_rgb)
        print(f"[debug] test_locations: {test_locations}")

        test_encoding = face_recognition.face_encodings(test_image_rgb)
        if len(test_encoding) > 0:
            known_encodings.append(test_encoding[0])
            known_names.append("Sahil")
            i = False
    #Convert BGR to RGB as face_recognition requires RGB
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

        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"
        if True in matches: 
            first_match_index = matches.index(True) 
            name = known_names[first_match_index]

        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 3) #Draws a rectangle around the face

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

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