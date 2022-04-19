#private関数は__
#メソッド、変数の頭は小文字、クラス名は
#pythonの命名規則

from this import d
import paho.mqtt.client
import json
import ssl
import datetime
import time
import alert

#openした時のログを保存するクラス
#非同期で動かしたいクラス↓
class Logger():

    global mqtt

    def __init__(self):
        self.mqtt = Mqtt()
        self.mqtt.connect()

    def __del__(self):
        del self.mqtt

    #ログの登録
    def write(self):
        #メッセージを作成
        tmstr = "{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
        json_msg = json.dumps({"GetDateTime": tmstr})
        #MQTT送信
        self.mqtt.publish(json_msg)         

#MQTT通信により、日時をDynamoDBに登録するクラス
class Mqtt():

    global client
    global mqtt_err_alert
    global is_connected

    #変数宣言
    AWSIOT_ENDPOINT = 'alij9rhkrwgll-ats.iot.ap-northeast-1.amazonaws.com'
    MQTT_PORT = 8883
    MQTT_TOPIC_PUB = "ksap-dooropener"
    MQTT_TOPIC_SUB = "ksap-dooropenerSub"
    MQTT_ROOTCA = "/home/pi/Downloads/AmazonRootCA1.pem"
    MQTT_CERT = "/home/pi/Downloads/2f8336dd1478dab6620ae585c583f4bbd851e1729eeecf119f5cd2e2e0ce8053-certificate.pem.crt"
    MQTT_PRIKEY = "/home/pi/Downloads/2f8336dd1478dab6620ae585c583f4bbd851e1729eeecf119f5cd2e2e0ce8053-private.pem.key"
    
    def __init__(self):

        self.is_connected = False

        # Mqtt Client Initialize
        self.client = paho.mqtt.client.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.tls_set(self.MQTT_ROOTCA, certfile=self.MQTT_CERT, keyfile=self.MQTT_PRIKEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        
        #アラートクラスのインスタンス
        self.mqtt_err_alert = alert.Alert("LED","RED")
    
    def __del__(self):
        del mqtt_err_alert
        self.client.disconnect()

    #初期接続
    def connect(self):
        # Connect To Mqtt Broker(aws)
        self.client.loop_start()

        try:
            self.client.connect(self.AWSIOT_ENDPOINT, port=self.MQTT_PORT, keepalive=5)
            self.mqtt_err_alert.stop()    
            self.is_connected = True
        except:
            print("Wi-Fi接続が切れています")
            self.mqtt_err_alert.start()    
            self.is_connected = False

    #MQTT接続イベント
    def __on_connect(self, client, userdata, flags, rc):
        self.is_connected = True
        #警告アラートを止める
        self.mqtt_err_alert.stop()

    #MQTT切断イベント
    def __on_disconnect(self, client, userdata, msg):
        print("MQTT切断")
        self.is_connected = False
        #警告アラートをスタートする
        self.mqtt_err_alert.start()

    def publish(self, json_msg): 
        #接続
        if self.is_connected == False:
            self.connect()
        #MQTT送信
        if self.is_connected:
           self.client.publish(self.MQTT_TOPIC_PUB ,json_msg, qos=1)
