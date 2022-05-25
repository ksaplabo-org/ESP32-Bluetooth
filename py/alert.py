import RPi.GPIO as GPIO

class Alert():
    """警告を行うクラス"""
    
    def __init__(self, type, color = "NONE"):
        if type == "LED":
            self.__alert = LedLigth(color)

    def __del__(self):
        del self.__alert

    #アラートを始めるメソッド
    def start_alert(self):
        self.__alert.start_led()
    #アラートを止めるメソッド
    def stop_alert(self):
        self.__alert.stop_led()

    #三色LED用のメソッド
    def start_center_alert(self):
        self.__alert.start_center_led()
    def stop_center_alert(self):
        self.__alert.stop_center_led()

class LedLigth():
    """LEDを扱うクラス"""

    #変数宣言
    CENTER_GREEN_LED = 27   #GPIOナンバー
    CENTER_BLUE_LED = 22    #GPIOナンバー
    RED_LED = 26            #GPIOナンバー
    GREEN_LED = 19          #GPIOナンバー
    BLUE_LED = 6            #GPIOナンバー

    def __init__(self, color):
        GPIO.setmode(GPIO.BCM)
        if color == "CENTER":
            self.__gpio_no = self.CENTER_GREEN_LED
            GPIO.setup(self.CENTER_BLUE_LED, GPIO.OUT)
        elif color == "RED":
            self.__gpio_no = self.RED_LED
        elif color == "GREEN":
            self.__gpio_no = self.GREEN_LED
        elif color == "BLUE":
            self.__gpio_no = self.BLUE_LED

        GPIO.setup(self.__gpio_no, GPIO.OUT)

        if color == "CENTER":
            #CENTERの緑は常時点灯
            GPIO.output(self.__gpio_no, True)

    def __del__(self):
        GPIO.cleanup()

    #LEDを点灯
    def start_led(self):
        #LEDをつける
        GPIO.output(self.__gpio_no, GPIO.HIGH)

    #LEDを消灯
    def stop_led(self):
        GPIO.output(self.__gpio_no, GPIO.LOW)

    #CENTERの時はGREEN→BLUEに変色
    def start_center_led(self):
        GPIO.output(self.__gpio_no, False)
        GPIO.output(self.CENTER_BLUE_LED, True)

    def stop_center_led(self):
        GPIO.output(self.CENTER_BLUE_LED, False)
        GPIO.output(self.__gpio_no, True)

