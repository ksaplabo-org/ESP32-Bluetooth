import board
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

FONT_SANS_12 = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc" ,12)
FONT_SANS_18 = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc" ,18)

class Display:
    """ディスプレイを操作するクラス"""

    def __init__(self):
        self.__i2c = board.I2C()
        self.__display = SSD1306_I2C(128, 64, board.I2C(), addr=0x3C)
        self.__count = 0

    def __del__(self):
        del self.__i2c
        del self.__display

    def draw_display(self, gender, age):
        """ディスプレイに性別と年齢を表示
        """
        img = Image.new("1",(self.__display.width, self.__display.height))
        draw = ImageDraw.Draw(img)
        draw.text((0,0),'性別 ' + gender,font=FONT_SANS_18,fill=1)
        draw.text((0,32),'年齢 ' + str(age),font=FONT_SANS_18,fill=1)

        self.__display.image(img)
        self.__display.show()
        self.__count = 0

    def refresh(self):
        self.__count = self.__count + 1
        if self.__count > 100:
            self.__display.fill(0)
            self.__display.show()
            self.__count = 0
