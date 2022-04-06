import cv2
import time

#カスケード分類器のパス
#以下のパスにhaarcascade_frontalface_alt.xmlがなければ、存在するパスを指定してください
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

    #顔と認識する場合は顔認識OKと出力
    if len(front_face_list) != 0:
        print("顔認識OK")
    else:
        print("顔認識NG")
    time.sleep(0.1)