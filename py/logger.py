from this import d

import paho.mqtt.client
import json
import ssl
import datetime
import time
import alert
import boto3
import board
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

i2c = board.I2C()
display = SSD1306_I2C(128, 64, board.I2C(), addr=0x3C)

FONT_SANS_12 = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc" ,12)
FONT_SANS_18 = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc" ,18)

class Logger():
    """現在時刻を登録するクラス"""

    def __init__(self):
        self.__mqtt = Mqtt()
        self.__mqtt.connect_mqtt()

    def __del__(self):
        del self.__mqtt

    def write_log(self,file_path,image_name):
        """ログの登録
        """

        #メッセージを作成
        tmstr = "{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
        json_msg = json.dumps({"GetDateTime": tmstr,"ImageName":image_name})
        #MQTT送信
        self.__mqtt.publish_mqtt(json_msg)
        self.__mqtt.writeS3(file_path,image_name)   

class Mqtt():
    """データをIoT Coreでpublishするクラス"""

    #変数宣言
    AWSIOT_ENDPOINT = 'alij9rhkrwgll-ats.iot.ap-northeast-1.amazonaws.com'
    MQTT_PORT = 8883
    MQTT_TOPIC_PUB = "ksap-dooropener"
    MQTT_TOPIC_SUB = "ksap-dooropenerSub"
    MQTT_ROOTCA = "/home/pi/Downloads/AmazonRootCA1.pem"
    MQTT_CERT = "/home/pi/Downloads/2f8336dd1478dab6620ae585c583f4bbd851e1729eeecf119f5cd2e2e0ce8053-certificate.pem.crt"
    MQTT_PRIKEY = "/home/pi/Downloads/2f8336dd1478dab6620ae585c583f4bbd851e1729eeecf119f5cd2e2e0ce8053-private.pem.key"

    def __init__(self):

        self.__is_connected = False

        # Mqtt Client Initialize
        self.__client = paho.mqtt.client.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__client.tls_set(self.MQTT_ROOTCA,
                              certfile=self.MQTT_CERT,
                              keyfile=self.MQTT_PRIKEY,
                              cert_reqs=ssl.CERT_REQUIRED,
                              tls_version=ssl.PROTOCOL_TLSv1_2,
                              ciphers=None)

        #アラートクラスのインスタンス
        self.__alert_mqtt_err = alert.LedAlert("RED")

    def __del__(self):
        del self.__alert_mqtt_err
        self.__client.disconnect()

    def connect_mqtt(self):
        """MQTT接続
        """

        # Connect To Mqtt Broker(aws)
        self.__client.loop_start()

        try:
            self.__client.connect(self.AWSIOT_ENDPOINT, port=self.MQTT_PORT, keepalive=5)
            self.__alert_mqtt_err.stop_alert()
            self.__is_connected = True
        except Exception:
            print("Wi-Fi接続が切れています")
            self.__alert_mqtt_err.start_alert()
            self.__is_connected = False

    #MQTT接続イベント
    def __on_connect(self, client, userdata, flags, rc):
        self.__is_connected = True
        #subscribe.topic set
        self.__client.subscribe(self.MQTT_TOPIC_SUB)
        #警告アラートを止める
        self.__alert_mqtt_err.stop_alert()

    #MQTT切断イベント
    def __on_disconnect(self, client, userdata, msg):
        print("MQTT切断")
        self.__is_connected = False
        #警告アラートをスタートする
        self.__alert_mqtt_err.start_alert()

    def publish_mqtt(self, json_msg): 
        """IoT Coreへパブリッシュを行う
        """

        if self.__is_connected is False:
            self.connect_mqtt()
        #MQTT送信
        if self.__is_connected:
            self.__client.publish(self.MQTT_TOPIC_PUB ,json_msg, qos=1)


    def __on_message(self,client, userdata, msg):
        result = json.loads(msg.payload)
        gender = '男性' if result["Gender"] == 'Male' else '女性'
        age = result["Age"]

        # draw image
        img = Image.new("1",(display.width, display.height))
        draw = ImageDraw.Draw(img)
        draw.text((0,0),'性別 ' + gender,font=FONT_SANS_18,fill=1)
        draw.text((0,32),'年齢 ' + str(age),font=FONT_SANS_18,fill=1)

        display.image(img)
        display.show()

    def writeS3(self,file_path,image_name):
        if self.__is_connected:
            bucket_name = "ksap-dooropener-image"
            s3 = boto3.resource('s3')
            s3.Bucket(bucket_name).upload_file(file_path+image_name,'img/'+image_name)
