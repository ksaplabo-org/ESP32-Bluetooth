import cv2
import time
import bluetooth

#開閉状態のフラグ初期化（True：空いている）
isOpen = False

#ESP32の定義
server_addr = 'ESP32のMACアドレス' 
server_port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((server_addr, server_port))

#カスケード分類器のパス
cascade_path="/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml"

#カスケード分類器を取得
cascade=cv2.CascadeClassifier(cascade_path) 

#カメラからの画像データの読み込み
capture = cv2.VideoCapture(0)

#リアルタイム静止画像の読み取りを繰り返す
while(True):
    #フレームの読み取り
    ret,frame=capture.read()

    #カメラから読み取った画像をグレースケールに変換
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #顔の学習データ精査
    front_face_list=cascade.detectMultiScale(gray,minSize=(50,50))
    print(front_face_list)
    #顔と認識する場合は顔認識OKと出力
    if len(front_face_list) != 0:
        print("顔認識OK")
        #紐を引っ張る
        sock.send('on')
        time.sleep(3)
    time.sleep(0.1)
