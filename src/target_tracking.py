import cv2
import os

detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

# detect target with HAAR algorithm
def target_detected(image):
	grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	detections = detector.detectMultiScale(grayscale_image, minNeighbors = 5)
	return detections[0] if len(detections) > 0 else None

# Calculate area of bounding box of target's face
def area(target):
	return target[2] * target[3]

# Examine if target is closer to the warehouse
def is_target_closer(target_prev, target):
	return area(target) > area(target_prev)
	
# Examine if target is farther from the warehouse
def is_target_farther(target_prev, target):
	return area(target) > area(target_prev)
	
# Examine if the target is too close to the warehouse
def is_target_too_close(target, tolerance):
	return area(target) > tolerance
