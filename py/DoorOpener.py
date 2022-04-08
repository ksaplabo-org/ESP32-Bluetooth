import cv2
import time
import bluetooth

#変数宣言
isSend = False      #送信フラグ
count = 0           #カウント値
fps = 30            #カメラのFPS
list = []           #顔認識5回分の結果記録配列
slowcount = 5       #顔認識していないことをスルーする回数

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
        isSend = True
        count = 0
        sock.send('on')
    if count < 70:
        count = count + 1
    else:
        isSend = False

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
        #配列変更
        ListChange(True)
        #ソケット送信
        SockSend()

    #顔認識してない場合
    else:
        #前5回の顔判定でOKがある場合
        if list.count(True) > 0:
            #ソケット送信
            SockSend()
            #配列変更
            ListChange(False)
        else:
            #配列変更
            ListChange(False)
            count = 0
            isSend = False
    
    #カメラのFPSと同じ速度でcapture.readを行う。
    time.sleep(fps/1000)

