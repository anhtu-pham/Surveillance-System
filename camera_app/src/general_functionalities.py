import time
import subprocess
import os
import cv2

def capture_image(camera, timestamp):
    image_path = "/media/ecse488-7/ESD-ISO/images/" + timestamp + ".jpg"
    camera.capture_file(image_path)
    return image_path
    
def compress_image(image_path, quality):
    cv2.imwrite(image_path, cv2.imread(image_path), [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    return image_path
    
def remove_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)
        print("Image " + image_path + " removed")
        
def capture_video(camera, encoder, timestamp, duration):
    video_path = "/media/ecse488-7/ESD-ISO/videos/" + timestamp + ".mpg"
    camera.start_recording(encoder, video_path)
    time.sleep(duration)
    camera.stop_recording()
    return video_path, timestamp
    
def write_log(file_path, log):
    with open(file_path, "a") as file:
        file.write("\n" + log)
