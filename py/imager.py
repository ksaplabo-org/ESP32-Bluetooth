from logging import captureWarnings
from tkinter import Frame

import time
import cv2
import alert
import datetime
import os

class ImgAnalysis():
    """画像解析クラス"""

    #定数宣言
    FPS = 30
    CASCADE_PATH = "/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml"
    MAX_LISE_FACE_RECOGNITION_RESULT = 5            #顔判定結果格納配列要素

    def __init__(self):

        #顔判定結果格納配列初期化
        self.__list_face_recognition_result = []

        #alertクラスのインスタンス
        self.__alert_camera_err = alert.LedAlert("GREEN")
        self.__alert_face_recognition = alert.ThreeColorLed()

        #カメラの設定
        self.__capture = cv2.VideoCapture(0)
        self.__capture.set(cv2.CAP_PROP_FPS, self.FPS)
        self.__capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.__capture.set(cv2.CAP_PROP_FRAME_WIDTH ,320)
        #self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))

        #カスケード分類器を取得
        self.__cascade = cv2.CascadeClassifier(self.CASCADE_PATH)

        #配列の初期化
        for _ in range(self.MAX_LISE_FACE_RECOGNITION_RESULT):
            self.__list_face_recognition_result = self.__list_face_recognition_result + [False]

    def __del__(self):
        self.__capture.release()
        del self.__alert_face_recognition

    def analyze_image(self):
        """画像解析を行う
        """

        #リアルタイム静止画像の読み取りを繰り返す
        try:
            #フレームの読み取り
            _,frame=self.__capture.read()
            #カメラから読み取った画像をグレースケールに変換
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            #顔の学習データ精査
            front_face_list=self.__cascade.detectMultiScale(gray,minSize=(50,50))
        except:
            #異常アラートを送信
            self.__alert_camera_err.start_alert()
            raise

        #異常アラートが出ていれば、止める
        self.__alert_camera_err.stop_alert()

        #認証結果を取得
        if len(front_face_list) != 0:
            result_face_recognition = True
        else:
            result_face_recognition = False

        #結果をlistに格納
        self.__list_face_recognition_result.pop(0)
        self.__list_face_recognition_result.insert(self.MAX_LISE_FACE_RECOGNITION_RESULT - 1,
                                                   result_face_recognition)
        file_path=""
        image_name=""
        #顔認証OK
        if result_face_recognition:
            #フレームに白枠を設定
            frame = self.__draw_rect(frame,front_face_list)
            #正常アラートを送信
            self.__alert_face_recognition.start_alert()
            now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            image_name ='image'+now+'.jpg'
            file_path='./workimg/'
            os.makedirs(file_path ,exist_ok=True)
            cv2.imwrite(file_path+image_name, frame)
        #顔認証NG
        else:
            #顔認証結果配列にTrueがある場合
            if self.__list_face_recognition_result.count(True) > 0:
                #顔認証したことにする
                result_face_recognition = True
            #アラートを止める
            self.__alert_face_recognition.stop_alert()
        #カメラ動画の表示
        cv2.imshow('capture',frame)
        cv2.waitKey(1)

        #capture.read()の調整
        time.sleep(self.FPS/1000)

        #顔認証の結果をMain処理に返す
        return result_face_recognition,file_path,image_name

    #取り込んだフレームに白枠の設定
    def __draw_rect(self, frame ,rect_list):
        for rect in rect_list:
            cv2.rectangle(
                frame,
                tuple(rect[0:2]),
                tuple(rect[0:2] + rect[2:4]),
                (255,255,255),
                thickness=2
            )
        return frame
