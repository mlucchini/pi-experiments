from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD


lcd = Adafruit_CharLCD(rs=26,  # Register Select
                       en=19,  # Enable
                       d4=13,  # LCD D4
                       d5=6,   # LCD D5
                       d6=5,   # LCD D6
                       d7=11,  # LCD D7
                       cols=16,
                       lines=2)

lcd.clear()
lcd.message('Et mamie tromblon\nElle tromblonne?')

while True:
    sleep(3)
    for _ in range(0, 16):
        lcd.move_right()
        sleep(.1)
    for _ in range(0, 16):
        lcd.move_left()
        sleep(.1)
