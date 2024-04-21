import time
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from camera_app.src.general_functionalities import capture_image, compress_image, remove_image, capture_video, write_log, manual_reset
from camera_app.src.target_tracking import target_detected

# Setup for camera and encoder
camera = Picamera2()
camera.start()
encoder = MJPEGEncoder()

image_path = None
target = None
print("Start")

time.sleep(10)

while target is None:
	timestamp = time.strftime("%m-%d-%Y,%H:%M:%S")
	image_path = capture_image(camera, timestamp)
	target = target_detected(image_path)
	if target is not None:
		print("Area ", target[2] * target[3])
	else:
		remove_image(image_path)
