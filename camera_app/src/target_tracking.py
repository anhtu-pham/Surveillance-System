import cv2
import os

detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

def target_detected(image_path):
	image = cv2.imread(image_path)
	grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	detections = detector.detectMultiScale(grayscale_image, minNeighbors = 5)
	return detections[0] if len(detections) > 0 else None

def area(target):
	return target[2] * target[3]

def is_target_closer(target_prev, target):
	return area(target) > area(target_prev)
	
def is_target_farther(target_prev, target):
	return area(target) > area(target_prev)
	
def is_target_too_close(target, limit):
	return area(target) > limit
