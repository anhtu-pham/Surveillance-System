import RPi.GPIO as GPIO
import time
import subprocess
import sqlite3
import cv2

# Setup for GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Setup for database
# db_connection = sqlite3.connect("database.db")
# cursor = db_connection.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS track(timestamp TEXT, state TEXT, data TEXT, message TEXT)")
# db_connection.commit()

def capture_image():
    timestamp = time.strftime("%m/%d/%Y:%H:%M:%S")
    image_path = "images/" + timestamp + ".jpg"
    subprocess.run(["libcamera-still", "-o"], image_path)
    return image_path, timestamp

def store_image(state, image_path, timestamp):
    message = "Store image"
    cv2.imwrite(image_path, cv2.imread(image_path), [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    # cursor.execute("INSERT INTO track(timestamp, state, data, message) VALUES (?, ?, ?)", (timestamp, state, image_path, message))
    # db_connection.commit()
    return image_path

# FSM
state = "S1" # initial state
try:
    while True:
        image_path, timestamp = capture_image()
        target = closest_target_detected(image_path)
        if state == "S1":
            if target is not None:
                state = "S2"
        
        elif state == "S2":
            if target is None:
                state = "S1"
            elif is_target_closer(before, after):
                state = "S3"

        elif state == "S3":
            if is_target_farther(before, after):
                state = "S2"
            elif is_target_too_close(tolerance):
                state = "S4"

        elif state == "S4":
            GPIO.output(18, GPIO.HIGH)
            time.sleep(10)
            GPIO.output(18, GPIO.LOW)
            if manual_reset():
                state = "S1"
        
        if state == "S1":
            time.sleep(1)
        elif state == "S2":
            store_image(image_path, state)
            time.sleep(0.5)
        elif state == "S3":
            store_image(image_path, state)
            time.sleep(0.125)
        elif state == "S4":
            capture_video()
            store_video(video_path)
            time.sleep(0.125)


except KeyboardInterrupt:
    pass