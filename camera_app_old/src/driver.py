import RPi.GPIO as GPIO
from gpiozero import Button
import time
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from general_functionalities import use_camera, capture_image, compress_image, remove_image, capture_video, write_log
from target_tracking import target_detected, is_target_closer, is_target_farther, is_target_too_close
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

    if state != "S4":
        image_path = capture_image(camera, current_camera_index, timestamp)
        target = target_detected(image_path)
        if state == "S1":
            if target is None:
                current_camera_index = 1 - current_camera_index
                use_camera(current_camera_index)
            else:
                state = "S2"
        elif state == "S2":
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
        time.sleep(1)
    elif state == "S2":
        write_log("../logs.txt", timestamp + ": Target detected by camera " + str(current_camera_index) + ".")
        print(image_path + ": Target detected at coordinates " + str(target))
        compress_image(image_path, 60)
        time.sleep(0.5)
    elif state == "S3":
        write_log("../logs.txt", timestamp + ": Target approaching the warehouse as recognized by camera " + str(current_camera_index) + ".")
        print(image_path + ": Approaching target at coordinates " + str(target))
        compress_image(image_path, 80)
        time.sleep(0.125)
    elif state == "S4":
        write_log("../logs.txt", timestamp + ": Suspicious target as recognized by camera " + str(current_camera_index) + ". Alarm!")
        print(image_path + ": Suspicious target at coordinates " + str(target))
        if not is_video_captured:
            capture_video(camera, current_camera_index, encoder, timestamp, 5)
            is_video_captured = True
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(0.5)
    else:
        pass
