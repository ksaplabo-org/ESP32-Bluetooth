import RPi.GPIO as GPIO
import warnings

#warnings.simplefilter('ignore')
#GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
#warnings.resetwarnings()

#変数宣言
CENTER_LED = 13      #GPIOナンバー
RED_LED = 26         #GPIOナンバー
GREEN_LED = 19       #GPIOナンバー
BLUE_LED = 6         #GPIOナンバー

try:
    GPIO.setmode(GPIO.BCM)
    #GPIO.cleanup()
    GPIO.setup(CENTER_LED ,GPIO.OUT)
    GPIO.setup(RED_LED ,GPIO.OUT)
    GPIO.setup(GREEN_LED ,GPIO.OUT)
    GPIO.setup(BLUE_LED ,GPIO.OUT)

    #GPIO.cleanup()

    GPIO.output(CENTER_LED ,GPIO.HIGH)
    GPIO.output(RED_LED ,GPIO.LOW)
    GPIO.output(GREEN_LED ,GPIO.LOW)
    GPIO.output(BLUE_LED ,GPIO.LOW)

finally:
    print('except')
    GPIO.cleanup()
