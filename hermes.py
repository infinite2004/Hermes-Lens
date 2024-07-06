import sys
import time
import cv2
import numpy as np
import pytesseract

from picamera import PiCamera
from picamera.array import PiRGBArray
from deep_translator import GoogleTranslator
#from langdetect import detect

#3/9/23 - 2 hours
#3/10/23-4 hours
#intialize hermes camera 
#3/13/23-4 hours - need tp update python version-- on step 8 if 7 was done
# error with version for opec cv when swtiched t0 3.8 or higher

Hermes_cam = PiCamera()
Hermes_cam.resolution = (640,480)
Hermes_cam.framerate = 60
Hermes_cam.rotation =  0
Hermes_cam.sharpness  =  50
rawCapture = PiRGBArray(Hermes_cam, size=(640,480))

#cam warmup
time.sleep(0.1)

#campture frames from the camera

for frame in Hermes_cam.capture_continuous(rawCapture, format = "bgr",use_video_port = True):

    image = frame.array
    
    text = pytesseract.image_to_string(image)
    #trasnlated_text = pytesseract.get_languages(image)


    #check if the detected langauge matches to a certain langauge and can translate that text
    """
    
    detected_text = detect(text)

    if detected_text == 'es':
        target_langauage = 'es'
    _________________________
    if the detected text is spanish then the text would be translated to spanish


    
    """
    final_text = GoogleTranslator(source='en',target='es').translate(text)
    
    cv2.imshow("Frame",image)
    
    #print(text)
    print(final_text)
    #print(trasnlated_text)
    
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("Q"):
        break
