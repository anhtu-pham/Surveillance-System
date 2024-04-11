import time
import subprocess
import os
import cv2

def capture_image(timestamp):
    image_path = "../images/" + timestamp + ".jpg"
    subprocess.run(["libcamera-still", "-o", image_path, "-t", "50"])
    return image_path
    
def compress_image(image_path, quality):
    message = "Compress image"
    cv2.imwrite(image_path, cv2.imread(image_path), [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    # cursor.execute("INSERT INTO track(timestamp, state, data, message) VALUES (?, ?, ?)", (timestamp, state, image_path, message))
    # db_connection.commit()
    return image_path
    
def remove_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)
        print("Image " + image_path + " removed")
        
def capture_video(timestamp, duration):
    video_path = "../videos/" + timestamp + ".mpg"
    subprocess.run(["libcamera-vid", "-o", video_path, "-t", str(duration)])
    return video_path, timestamp
    
def write_log(file_path, log):
    with open(file_path, "a") as file:
        file.write(log + "\n ")
        
def manual_reset():
    return False
