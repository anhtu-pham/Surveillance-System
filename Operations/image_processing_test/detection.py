import cv2

def detect_human(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained Haar cascade for human face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # If any faces are detected, return True (human detected)
    if len(faces) > 0:
        return True
    else:
        return False

x = detect_human (/Users/j.aloufi/Documents/PhD/Spring 2024/ECSE 488/Surveillance-System/Operations/image_processing_test/234DF59E4A5A4795814AC0D93EE9EAE6.jpg.jpeg)

print(x) 