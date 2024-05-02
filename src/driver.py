import RPi.GPIO as GPIO
from gpiozero import Button
import time
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from general_functionalities import use_camera, capture_image, compress_image, remove_image, capture_video, write_log
from target_tracking import target_detected, is_target_closer, is_target_farther, is_target_too_close
import cv2
# import os

# Setup for GPIO
BUZZER_PIN = 21
MANUAL_RESET_PIN = 20
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Buzzer
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Multiple cameras
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

# Manual reset button
button = Button(MANUAL_RESET_PIN)


# Setup for camera
camera = Picamera2()
camera.start()
encoder = MJPEGEncoder()

# FSM
state = "S1" # initial state

is_video_captured = False
image_path = None
target = None
target_prev = None
tolerance_threshold = 10
undetected_count = 0
farther_threshold = 10
farther_count = 0
current_camera_index = 0
is_from_state_1 = False
color = None

def when_pressed():
    global state, is_video_captured
    if state == "S4":
        timestamp = time.strftime("%m-%d-%Y_%H-%M-%S")
        write_log("../logs.txt", timestamp + ": User performed manual reset!")
        state = "S1"
        is_video_captured = False

button.when_pressed = when_pressed
use_camera(current_camera_index)
while True:
        
    timestamp = time.strftime("%m-%d-%Y_%H-%M-%S")
    image_path = capture_image(camera, current_camera_index, timestamp)
    image = cv2.imread(image_path)
    target = target_detected(image)

    if state == "S1":

        if target is None:
            current_camera_index = 1 - current_camera_index
            use_camera(current_camera_index)
        else:
            state = "S2"
            is_from_state_1 = True
            
    else:
        if is_from_state_1:
            cv2.namedWindow("Real Time Image Display", cv2.WINDOW_NORMAL)
            is_from_state_1 = False
        
        if state == "S2":
            if target is None: # target currently not detected
                undetected_count += 1
                # decision on no target detected for certain times
                if undetected_count > tolerance_threshold:
                    state = "S1"
                    undetected_count = 0
                # can have further detections before decision
                else:
                    continue
            else: # target detected
                undetected_count = 0
                if is_target_closer(target_prev, target) and is_target_too_close(target, 2000):
                    state = "S3"
        elif state == "S3":
            if target is None: # target currently not detected
                undetected_count += 1
                # decision on no target detected for certain times
                if undetected_count > tolerance_threshold:
                    state = "S2"
                    undetected_count = 0
                    farther_count = 0
                # can have further detections before decision
                else:
                    continue
            else: # target detected
                undetected_count = 0
                if is_target_farther(target_prev, target):
                    farther_count += 1
                    if farther_count > farther_threshold:
                        state = "S2"
                        farther_count = 0
                else:
                    farther_count = 0
                    if is_target_too_close(target, 4500):
                        state = "S4"
        else:
            pass
    target_prev = target if target is not None else target_prev
        
    if state == "S1":
        remove_image(image_path)
        print("Safe state with camera " + str(current_camera_index) + ".")
        time.sleep(0.2)
    else:
        if state == "S2":
            color = (255, 0, 0)
            write_log("../logs.txt", timestamp + ": Target detected by camera " + str(current_camera_index) + ".")
            print(timestamp + ": Target detected by camera " + str(current_camera_index) + ".")
            compress_image(image_path, 60)
            time.sleep(0.1)
        elif state == "S3":
            color = (0, 255, 255)
            write_log("../logs.txt", timestamp + ": Target approaching the warehouse as recognized by camera " + str(current_camera_index) + ".")
            print(timestamp + ": Target approaching the warehouse as recognized by camera " + str(current_camera_index) + ".")
            compress_image(image_path, 80)
            time.sleep(0.05)
        elif state == "S4":
            color = (0, 0, 255)
            write_log("../logs.txt", timestamp + ": Suspicious target as recognized by camera " + str(current_camera_index) + ". Alarm!")
            print(timestamp + ": Suspicious target as recognized by camera " + str(current_camera_index) + ". Alarm!")
            if not is_video_captured:
                capture_video(camera, current_camera_index, encoder, timestamp, 2)
                is_video_captured = True
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.1)
        else:
            continue
        if target is not None:
            (x, y, w, h) = target
            cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
        cv2.imshow("Real Time Image Display", image)
        cv2.waitKey(1)
