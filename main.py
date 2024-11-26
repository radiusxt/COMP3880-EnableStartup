import numpy
import cv2
import sys
sys.path.append("/home/pi/.local/pipx/venvs/face-recognition/lib/python3.11/site-packages")
import face_recognition


image = face_recognition.load_image_file("DSC04401.JPG")
#video_capture = cv2.VideoCapture(0)
face_locations = face_recognition.face_locations(image) # a list of box coordinates, [(top, right, bottom, left), ...]

# Convert to BGR for OpenCV (optional, as OpenCV uses BGR format)
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# Draw rectangles around faces
for (top, right, bottom, left) in face_locations:
    cv2.rectangle(image, (left, top), (right, bottom), (255, 255, 0), 3)

# Display the result
cv2.imshow("Image", image)
cv2.waitKey(0)
#video_capture.release()
cv2.destroyAllWindows()