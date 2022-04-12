import cv2
import time
import bluetooth
import select
import paho.mqtt.client
import json
import datetime
import RPi.GPIO as GPIO
import ssl
import os

list = []
isSend = False
isSendRet = False
count = 0
slowcount = 5

PIN_LED1 = 26
PIN_LED2 = 6

#Mqtt Define
AWSIoT_ENDPOINT = 'alij9rhkrwgll-ats.iot.ap-northeast-1.amazonaws.com'
MQTT_PORT = 8883
MQTT_TOPIC_PUB = "ksap-dooropener"
MQTT_TOPIC_SUB = "ksap-dooropenerSub"
MQTT_ROOTCA = "/home/pi/Downloads/AmazonRootCA1.pem"
MQTT_CERT = "/home/pi/Downloads/2f8336dd1478dab6620ae585c583f4bbd851e1729eeecf119f5cd2e2e0ce8053-certificate.pem.crt"
MQTT_PRIKEY = "/home/pi/Downloads/2f8336dd1478dab6620ae585c583f4bbd851e1729eeecf119f5cd2e2e0ce8053-private.pem.key"

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_LED1 ,GPIO.OUT)
GPIO.setup(PIN_LED2 ,GPIO.OUT)

def mqtt_connect(client, userdata, flags, respons_code):
    print('mqtt connected.')
    # Entry Mqtt Subscribe.
    client.subscribe(MQTT_TOPIC_SUB)
    print('subscribe topic : ' + MQTT_TOPIC_SUB)

def mqtt_message(client, userdata, msg):
    # Get Received Json Data
    json_dict = json.loads(msg.payload)
    # if use ... json_dict['xxx']

#配列の初期化
for num in range(slowcount):
    list = list + [False]

#配列操作の関数(引数：顔認証OK→True、顔認証NG→False)
def ListChange(bool):
    global list
    list.pop(0)
    list.insert(slowcount - 1, bool)

#Bluetootshsソケット送信関数
def SockSend():
    global isSend
    global count

    #一度'on'を送信したら約7秒間は顔認証しても'on'を送らない
    if not(isSend):
        try:
            isSend = True
            count = 0
            sock.send('on')

            #現在日時の取得
            tm = datetime.datetime.now()
            #送信メッセージの作成
            tmstr = "{0:%Y-%m-%d %H:%M:%S}".format(tm)
            json_msg = json.dumps({"GetDateTime": tmstr})
            #MQTT送信
            client.publish(MQTT_TOPIC_PUB ,json_msg, qos=1)
            #LED.ON
            GPIO.output(PIN_LED1 ,GPIO.HIGH)
            #REDLED.OFF
            GPIO.output(PIN_LED2 ,GPIO.LOW)

        #BluetoothまたはMQTT送信失敗時
        except:
            print('BluetoothまたはMQTT送信失敗')
            #REDLED.ON
            GPIO.output(PIN_LED2 ,GPIO.HIGH)

    if count < 70:
        count = count + 1
    else:
        isSend = False

#カメラのFPS
fps = 30

#ESP32の定義
server_addr = '7C:9E:BD:48:46:6A' #MACアドレス
server_port = 1

#接続できない場合は、処理を止める
try:
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((server_addr, server_port))
except :
    print('接続できるESP32がありません')
    os.eixt()

#カスケード分類器のパス
cascade_path="/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml"

#カスケード分類器を取得
cascade=cv2.CascadeClassifier(cascade_path)

#カメラからの画像データの読み込み
capture = cv2.VideoCapture(0)

#カメラの設定
capture.set(cv2.CAP_PROP_FPS, fps)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
capture.set(cv2.CAP_PROP_FRAME_WIDTH ,320)
capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))

# Mqtt Client Initialize
client = paho.mqtt.client.Client()
client.on_connect = mqtt_connect
client.on_message = mqtt_message
client.tls_set(MQTT_ROOTCA, certfile=MQTT_CERT, keyfile=MQTT_PRIKEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# Connect To Mqtt Broker(aws)
client.connect(AWSIoT_ENDPOINT, port=MQTT_PORT, keepalive=60)

#取り込んだフレームに白枠の設定
def drawRect(frame ,rect_list):
    for rect in rect_list:
        cv2.rectangle(
            frame,
            tuple(rect[0:2]),
            tuple(rect[0:2] + rect[2:4]),
            (255,255,255),
            thickness=2
        )
    return frame

#リアルタイム静止画像の読み取りを繰り返す
while(True):
    try:
        #フレームの読み取り
        ret,frame=capture.read()

        #カメラから読み取った画像をグレースケールに変換
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        #顔の学習データ精査
        front_face_list=cascade.detectMultiScale(gray,minSize=(50,50))
    except:
        print('CameraErr Or Ctrl+C')
        break

    #顔と認識する場合は顔認識OKと出力
    if len(front_face_list) != 0:
        print("顔認識OK")
        #print(count)
        frame = drawRect(frame,front_face_list)
        #配列変更
        ListChange(True)
        #ソケット送信
        isSendRet = SockSend()

    else:
        #前5回の顔判定でOKがある場合
        if list.count(True) > 0:
            #ソケット送信
            isSendRet = SockSend()
            #配列変更
            ListChange(False)
            continue

        ListChange(False)
        print("顔認識NG")
        count = 0
        isSend = False

        #LED.OFF
        GPIO.output(PIN_LED1 ,GPIO.LOW)
        GPIO.output(PIN_LED2 ,GPIO.LOW)

    #カメラ動画の表示
    cv2.imshow('capture',frame)
    cv2.waitKey(1)

    time.sleep(fps/1000)
