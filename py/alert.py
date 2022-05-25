import RPi.GPIO as GPIO
from abc import ABC, abstractmethod, ABCMeta

class Alert(metaclass=ABCMeta):
    """警告を行う抽象クラス"""

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    def __del__(self):
        GPIO.cleanup()

    @abstractmethod
    def start_alert(self):
        pass

    @abstractmethod
    def stop_alert(self):
        pass

class LedAlert(Alert):
    """LEDを扱うクラス"""

    #変数宣言
    RED_LED = 26            #GPIOナンバー
    GREEN_LED = 19          #GPIOナンバー
    BLUE_LED = 6            #GPIOナンバー

    def __init__(self, color):

        super().__init__()

        if color == "RED":
            self.__gpio_no = self.RED_LED
        elif color == "GREEN":
            self.__gpio_no = self.GREEN_LED
        elif color == "BLUE":
            self.__gpio_no = self.BLUE_LED

        GPIO.setup(self.__gpio_no, GPIO.OUT)

    def start_alert(self):
        """LEDを点灯
        """
        GPIO.output(self.__gpio_no, GPIO.HIGH)

    def stop_alert(self):
        """LEDを消灯
        """
        GPIO.output(self.__gpio_no, GPIO.LOW)

class ThreeColorLed(Alert):
    """3色LEDを扱うクラス"""

    CENTER_GREEN_LED = 27   #GPIOナンバー
    CENTER_BLUE_LED = 22    #GPIOナンバー

    def __init__(self):
        super().__init__()
        GPIO.setup(self.CENTER_GREEN_LED, GPIO.OUT)
        GPIO.setup(self.CENTER_BLUE_LED, GPIO.OUT)

    def start_alert(self):
        GPIO.output(self.CENTER_GREEN_LED, False)
        GPIO.output(self.CENTER_BLUE_LED, True)

    def stop_alert(self):
        GPIO.output(self.CENTER_BLUE_LED, False)
        GPIO.output(self.CENTER_GREEN_LED, True)
