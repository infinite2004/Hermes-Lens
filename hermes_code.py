import smbus
import time 
from picamera  import PiCamera
from picamera.array import PiRGBArray
#from deep_translator import GoogleTranslator
import cv2
import time
import pytesseract
import numpy as np
from deep_translator import GoogleTranslator
from langdetect import detect 


I2C_ADDR = 0x27 #I2C device paramertes 
LCD_WIDTH = 16 # MAX characyers per line

# define some of the parameters

LCD_CHR = 1 #mode--sending data 
LCD_CMD = 0 # mode -- sending command

LCD_LINE_1 = 0x80 #lcd ram address for line 1
LCD_LINE_2 = 0xC0 #lcd ram address for line 2
LCD_LINE_3 = 0x94 #lcd ram address for line 3
LCD_LINE_4 = 0xD4 #lcd ram address for line 4

LCD_BACKLIGHT = 0x08 #om
ENABLE = 0b00000100# enable bit 

#timing constants
E_PULESE = 0.0005
E_DELAY = 0.0005 


#open I2C interface
bus = smbus.SMBus(1)


def lcd_init():
    #initialize display
    lcd_byte(0x33,LCD_CMD) #110011 initalise 
    lcd_byte(0x32,LCD_CMD) # 110010 initalise 
    lcd_byte(0x06,LCD_CMD) # 000110 curspr move drection
    lcd_byte(0x0C,LCD_CMD) # 001100 display on. cursor off/ blink off
    lcd_byte(0x28,LCD_CMD) #101000 data ;ength, numver of lines, font size 
    lcd_byte(0x01,LCD_CMD) # 000001 clear display
    time.sleep(E_DELAY)

def lcd_byte(bits,mode):

    #send byte to data pins 
    #bits -- the data
    #mode -- 1 for data 
    #0 for command 
    
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT

    bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT


#high bits
    bus.write_byte(I2C_ADDR,bits_high)
    lcd_toggle_enable(bits_high)
#low bits
    bus.write_byte(I2C_ADDR,bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    #toggle enabled 

        time.sleep(E_DELAY)
        bus.write_byte(I2C_ADDR,(bits | ENABLE))
        time.sleep(E_PULESE)
        bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
        time.sleep(E_DELAY)

def lcd_string(message,line):
    #send string to display

     message =  message.ljust(LCD_WIDTH," ")

     lcd_byte(line, LCD_CMD)

     for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

def main():
    
    lcd_init() #initaLISE
    Hermes_cam = PiCamera()

    while True:
        #code fpr picamera -- initailized camera 

        Hermes_cam.resolution = (640,480)
        Hermes_cam.framerate = 60
        Hermes_cam.rotation =  0
        Hermes_cam.sharpness  =  50
        rawCapture = PiRGBArray(Hermes_cam, size=(640,480))

        #cam warmup
        time.sleep(0.1)
        

        #campture frames from the camera
        #rawCapture = PiRGBArray(Hermes_cam, size=(640,480))-raw_cap_indent error

        for frame in Hermes_cam.capture_continuous(rawCapture, format = "bgr",use_video_port = True):

            image = frame.array
    
            text = pytesseract.image_to_string(image)# this text variable is what stores the data from the camera
            #trasnlated_text = pytesseract.get_languages(image)
            
            try:
        
                detected_lang = detect(text)
            except:
                detected_lang='en' 

            if detected_lang !="en":
                final_text = GoogleTranslator(source=detected_lang,target='en').translate(text)
            else:
                final_text=text
    
             
            lcd_string(final_text,LCD_LINE_1) # tried to print the text from pi camera on ;cd sreen
             
            lcd_string(""*LCD_WIDTH,LCD_LINE_2)
            
            cv2.imshow("Frame",image)
    
            #print(text)
            #print(trasnlated_text)
             #prints text to terminal
            print(final_text)
            
            key = cv2.waitKey(1) & 0xFF
            rawCapture.truncate(0)
            if key == ord("Q"):
                continue
            
                

        
       

         #time.sleep(3)
        #sending some text
       # lcd_string("yooo", LCD_LINE_1)
      #  lcd_string("does", LCD_LINE_2)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01,LCD_CMD)
        
#PROJECT FINISHED 3/24/23..

