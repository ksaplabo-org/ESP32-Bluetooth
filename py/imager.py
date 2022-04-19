from logging import captureWarnings
from tkinter import Frame
import cv2
import time
import alert

#画像処理クラス
class ImgAnalysis():

    global camera_alert
    global face_alert
    global capture
    global cascade

    fps = 30
    cascade_path = "/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml"
    face_result_list = []   #顔判定結果格納配列
    list_max = 5            #顔判定結果格納配列要素数

    #コンストラクタ
    def __init__(self):

        #alertクラスのインスタンス
        self.camera_err_alert = alert.Alert("LED","GREEN")
        self.face_alert = alert.Alert("LED","CENTER")

        #カメラの設定
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FPS, self.fps)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH ,320)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
        
        #カスケード分類器を取得
        self.cascade = cv2.CascadeClassifier(self.cascade_path)

        #配列の初期化
        for num in range(self.list_max):
            self.face_result_list = self.face_result_list + [False]

    def __del__(self):
        self.capture.release()
        del self.face_alert

    #画像解析
    def img_analysis(self):

        #リアルタイム静止画像の読み取りを繰り返す
        try:
            #フレームの読み取り
            ret,frame=self.capture.read()
            #カメラから読み取った画像をグレースケールに変換
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   
            #顔の学習データ精査
            front_face_list=self.cascade.detectMultiScale(gray,minSize=(50,50))
        except:
            #異常アラートを送信
            self.camera_err_alert.start()
            raise

        #異常アラートが出ていれば、止める
        self.camera_err_alert.stop()

        #認証結果を取得
        if len(front_face_list) != 0:
            result = True
        else:
            result = False
        
        #結果をlistに格納
        self.face_result_list.pop(0)
        self.face_result_list.insert(self.list_max - 1, result)

        #顔認証OK
        if result:
            #フレームに白枠を設定
            frame = self.draw_rect(frame,front_face_list)
            #正常アラートを送信
            self.face_alert.start()

        #顔認証NG
        else:
            #顔認証結果配列にTrueがある場合
            if self.face_result_list.count(True) > 0:
                #顔認証したことにする
                result = True
            #アラートを止める
            self.face_alert.stop()
        
        #カメラ動画の表示
        cv2.imshow('capture',frame)
        cv2.waitKey(1)

        #capture.read()の調整
        time.sleep(self.fps/1000)

        #顔認証の結果をMain処理に返す
        return result

    #取り込んだフレームに白枠の設定
    def draw_rect(self, frame ,rect_list):
        for rect in rect_list:
            cv2.rectangle(
                frame,
                tuple(rect[0:2]),
                tuple(rect[0:2] + rect[2:4]),
                (255,255,255),
                thickness=2
            )
        return frame
