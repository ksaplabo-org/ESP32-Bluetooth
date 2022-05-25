import RPi.GPIO as GPIO

class Alert():
    """警告を行うクラス"""

    def __init__(self, type, color = "NONE"):
        if type == "LED":
            self.__alert = LedLigth(color)

    def __del__(self):
        del self.__alert

    def start_alert(self):
        """アラートを始めるメソッド
        """
        self.__alert.start_led()

    def stop_alert(self):
        """アラートを止めるメソッド
        """
        self.__alert.stop_led()

    def start_center_alert(self):
        """三色LED用のメソッド
        """
        self.__alert.start_center_led()

    def stop_center_alert(self):
        """三色LED用のメソッド
        """
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

    def start_led(self):
        """LEDを点灯
        """
        GPIO.output(self.__gpio_no, GPIO.HIGH)

    def stop_led(self):
        """LEDを消灯
        """
        GPIO.output(self.__gpio_no, GPIO.LOW)

    def start_center_led(self):
        """CENTERの時は3色LEDをGREEN→BLUEに変色
        """
        GPIO.output(self.__gpio_no, False)
        GPIO.output(self.CENTER_BLUE_LED, True)

    def stop_center_led(self):
        """3色LEDをBLUE→GREENに変色
        """
        GPIO.output(self.CENTER_BLUE_LED, False)
        GPIO.output(self.__gpio_no, True)
