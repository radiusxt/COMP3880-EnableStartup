"""import numpy as np
import cv2
import sys
sys.path.append("/home/pi/.local/pipx/venvs/face-recognition/lib/python3.11/site-packages")
import face_recognition



image = face_recognition.load_image_file("DSC04929.JPG")
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



video_capture = cv2.VideoCapture(0)
process_frame = True

# Loop runs indefinitely until KeyboardInterrupt
while True:
    ret, frame = video_capture.read()

    # Process each alternating frame
    if process_frame:

        # Resize frame to 1/4 resolution
        downscaled_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        downscaled_frame_rgb = downscaled_frame[:, :, :: -1]

        # Identify all faces in the current frame and store its box location
        face_locations = face_recognition.face_locations(downscaled_frame_rgb, model="hog")

        # Loop through all identified faces
        for (top, right, bottom, left) in face_locations:
            # Upscale the face locations after downscaling the image for processing
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom + 50), (255, 255, 0), 3)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom), (right, bottom + 50), (255, 255, 0), cv2.FILLED)

        # Display resulting image
        cv2.imshow('Video', frame)

    process_frame = not process_frame

    # Hit 'Q' on the keyboard to stop the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam and any open windows
video_capture.release()
cv2.destroyAllWindows()
"""


# with multiprocessing
import face_recognition
import cv2
import os
from multiprocessing import Pool, cpu_count

# Worker function to process each image
def process_image(image_path):
    try:
        # Load the image
        image = face_recognition.load_image_file(image_path)
        
        # Find all face locations
        face_locations = face_recognition.face_locations(image, model="hog")
        
        # Log results
        print(f"Found {len(face_locations)} face(s) in {image_path}")
        
        # Annotate image with rectangles around faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)
        
        # Save the annotated image
        output_path = f"output_{os.path.basename(image_path)}"
        cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        
        return image_path, len(face_locations)
    except Exception as e:
        return image_path, f"Error: {str(e)}"

# Main function to handle multiprocessing
def main(input_directory):
    # Get a list of image paths
    image_paths = [
        os.path.join(input_directory, f)
        for f in os.listdir(input_directory)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]
    
    # Use all available CPU cores
    num_cores = cpu_count()
    print(f"Using {num_cores} cores")
    
    # Create a Pool of workers
    with Pool(processes=num_cores) as pool:
        # Process images in parallel
        results = pool.map(process_image, image_paths)
    
    # Print the results
    for image_path, status in results:
        print(f"{image_path}: {status}")

if __name__ == "__main__":
    # Directory containing input images
    input_directory = "./pictures_of_people_i_know"
    
    main(input_directory)
