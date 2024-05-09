import time
import subprocess
import os
import cv2
import RPi.GPIO as GPIO

def use_camera(camera_index):
    if camera_index == 0:
        os.system("i2cset -y 1 0x70 0x00 0x04")
        GPIO.output(4, False)
        GPIO.output(17, False)
        GPIO.output(18, True)
    else:
        os.system("i2cset -y 1 0x70 0x00 0x06")
        GPIO.output(4, False)
        GPIO.output(17, True)
        GPIO.output(18, False)

# Capture image by current camera at current timestamp
def capture_image(camera, current_camera_index, timestamp):
    image_path = "/media/ecse488-7/group7/images/camera_" + str(current_camera_index) + "_time_" + timestamp + ".jpg"
    camera.capture_file(image_path)
    return image_path
    
# Compress image for efficient storage
def compress_image(image_path, quality):
    cv2.imwrite(image_path, cv2.imread(image_path), [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    return image_path
    
# Remove unnecessary image
def remove_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)
        
# Capture video by current camera with specified encoder from current timestamp for specified duration
def capture_video(camera, current_camera_index, encoder, timestamp, duration):
    video_path = "/media/ecse488-7/group7/videos/camera_" + str(current_camera_index) + "_time_" + timestamp + ".mpg"
    camera.start_recording(encoder, video_path)
    time.sleep(duration)
    camera.stop_recording()
    camera.start()
    return video_path, timestamp
    
# Write log message to logs file
def write_log(file_path, log):
    with open(file_path, "a") as file:
        file.write("\n" + log)
