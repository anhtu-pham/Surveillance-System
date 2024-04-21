import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from camera_app.src.general_functionalities import capture_image, compress_image, remove_image, capture_video, write_log, manual_reset
from camera_app.src.target_tracking import target_detected, is_target_closer, is_target_farther, is_target_too_close
import keyboard

# Setup for GPIO
BUZZER_PIN = 21
MANUAL_RESET_PIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(MANUAL_RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup for camera and encoder
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
        
def on_key_event(event):
    global state
    if event.name == 'r' and state == "S4":
        timestamp = time.strftime("%m-%d-%Y,%H:%M:%S")
        write_log("../logs.txt", timestamp + ": User performed manual reset by pressing R!")
        state = "S1"
        is_video_captured = False

keyboard.on_press(on_key_event)

while True:
        
    timestamp = time.strftime("%m-%d-%Y,%H:%M:%S")
        
    if state != "S4":
            # pass
            # if global_var.manual_reset:
            #    state = "S1"
            #    is_video_captured = False
            #    global_var.manual_reset = False
    # else:
        image_path = capture_image(camera, timestamp)
        target = target_detected(image_path)
        if state == "S1":
            if target is not None:
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
        write_log("../logs.txt", timestamp + ": Target detected.")
        print(image_path + ": Target detected at coordinates " + str(target))
        compress_image(image_path, 60)
        time.sleep(0.5)
    elif state == "S3":
        write_log("../logs.txt", timestamp + ": Target approaching the warehouse.")
        print(image_path + ": Approaching target at coordinates " + str(target))
        compress_image(image_path, 80)
        time.sleep(0.125)
    elif state == "S4":
        write_log("../logs.txt", timestamp + ": Suspicious target. Alarm!")
        print(image_path + ": Suspicious target at coordinates " + str(target))
        if not is_video_captured:
            capture_video(camera, encoder, timestamp, 5)
            is_video_captured = True
        GPIO.output(21, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(21, GPIO.LOW)
        time.sleep(0.5)
    else:
        pass
