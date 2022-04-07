import cv2
import time
import bluetooth

#変数宣言
isSend = False   #送信フラグ
count = 0        #カウント値
fps = 30         #カメラのFPS

#ESP32の定義
server_addr = '7C:9E:BD:48:46:6A' #MACアドレス
server_port = 1

#Bluetoothライブラリの初期化
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((server_addr, server_port))

#カスケード分類器のパス
cascade_path="/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml"

#カスケード分類器を取得
cascade=cv2.CascadeClassifier(cascade_path)

#カメラからの画像データの読み込み
capture = cv2.VideoCapture(0)

#FPSの設定
capture.set(cv2.CAP_PROP_FPS, fps)

#リアルタイム静止画像の読み取りを繰り返す
while(True):
    #フレームの読み取り
    ret,frame=capture.read()

    #カメラから読み取った画像をグレースケールに変換
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #顔の学習データ精査
    front_face_list=cascade.detectMultiScale(gray,minSize=(50,50))

    #顔認識した場合
    if len(front_face_list) != 0:
        #ソケット送信
        if not(isSend):
            isSend = True
            count = 0
            sock.send('on')
        #約７秒間はソケット送信しない
        if count < 70:
            count = count + 1
        else:
            isSend = False
    #顔認識してない場合
    else:
        count = 0
        isSend = False
    time.sleep(fps/1000)

