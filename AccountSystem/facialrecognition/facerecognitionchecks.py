import cv2 
import os   

def webcam_check():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("No webcam found. Exiting...")

def image_check():
    # check if this file exists 'AccountSystem/facialrecognition/captured_image.jpg'
    if os.path.isfile('AccountSystem/facialrecognition/captured_image.jpg'):
        print("Captured image found.")
        return False
    else:
        print("Captured image not found. Exiting...")
        return True