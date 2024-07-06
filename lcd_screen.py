import smbus
import time 


I2C_ADDR = 0x27
LCD_WIDTH = 16

# define some of the parameters

LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80 
LCD_LINE_2 = 0xC0
LCD_LINE_3 = 0x94
LCD_LINE_4 = 0xD4

LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100

E_PULESE = 0.0005
E_DELAY = 0.0005 

bus = smbus.SMBus(1)


def lcd_init():
    lcd_byte(0x33,LCD_CMD)
    lcd_byte(0x32,LCD_CMD)
    lcd_byte(0x06,LCD_CMD)
    lcd_byte(0x0C,LCD_CMD)
    lcd_byte(0x28,LCD_CMD)
    lcd_byte(0x01,LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits,mode):
    
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT

    bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(I2C_ADDR,bits_high)
    lcd_toggle_enable(bits_high)

    bus.write_byte(I2C_ADDR,bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
        time.sleep(E_DELAY)
        bus.write_byte(I2C_ADDR,(bits | ENABLE))
        time.sleep(E_PULESE)
        bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
        time.sleep(E_DELAY)

def lcd_string(message,line):

     message =  message.ljust(LCD_WIDTH," ")

     lcd_byte(line, LCD_CMD)

     for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

def main():
    lcd_init()

    while True:

     lcd_string("RPi LCD TUTORIAL",LCD_LINE_1)
     lcd_string(" YOOOO ",LCD_LINE_2)

     time.sleep(3)

     lcd_string("It works", LCD_LINE_1)
     lcd_string(" Hermes Translator ", LCD_LINE_2)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01,LCD_CMD)
