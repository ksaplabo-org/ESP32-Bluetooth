import RPi.GPIO as GPIO

#LEDに関するクラス
class Alert():

    global alert

    #コンストラクタ
    def __init__(self, type, color = "NONE"):
        if type == "LED":
            self.alert = LedLigth(color)

    def __del__(self):
        del self.alert

    #アラートを始めるメソッド
    def start(self):
        self.alert.start()
    #アラートを止めるメソッド
    def stop(self):
        self.alert.stop()

#LEDライトを使用するクラス
class LedLigth():

    #変数宣言
    CENTER_LED = 13      #GPIOナンバー
    RED_LED = 26         #GPIOナンバー
    GREEN_LED = 19       #GPIOナンバー
    BLUE_LED = 6         #GPIOナンバー

    global color
    global gpio_no

    #コンストラクタ
    def __init__(self, color):
        GPIO.setmode(GPIO.BCM)
        if color == "CENTER":    
            self.gpio_no = self.CENTER_LED
        elif color == "RED":
            self.gpio_no = self.RED_LED
        elif color == "GREEN":
            self.gpio_no = self.GREEN_LED
        elif color == "BLUE":
            self.gpio_no = self.BLUE_LED
        
        GPIO.setup(self.gpio_no ,GPIO.OUT)

    def __del__(self):
        GPIO.cleanup()

    #LEDを点灯
    def start(self):
        #LEDをつける
        GPIO.output(self.gpio_no ,GPIO.HIGH)

    #LEDを消灯
    def stop(self):
        GPIO.output(self.gpio_no ,GPIO.LOW)