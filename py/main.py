from email.headerregistry import Address

import time
import logger           #ログ登録クラス
import opener           #ドア開錠クラス
import imager           #画像解析クラス

__logger = logger.Logger()
__opener = opener.Opener(ADDR='78:21:84:80:2f:aa',PORT=1)
__imager = imager.ImgAnalysis()

try:
    #リアルタイム静止画像の読み取りを繰り返す
    while(True):

        try:
            #顔認証行う
            result,file_path,image_name = __imager.analyze_image()
        except Exception:
            #異常終了の場合
            print('CameraErr')
            time.sleep(1)

            #インスタンスを削除し、再生成
            del __imager
            __imager = imager.ImgAnalysis()

            continue

        #顔認識した場合
        if result is True:
            #print("顔認識OK")
            #ドアOpen
            if __opener.open():
                #Openした時のログを保持
                __logger.write_log(file_path,image_name)

        #顔認証してない場合
        else:
            #print("顔認証NG")
            #初期化
            __opener.reset_counter()

        #ディスプレイ表示更新
        __logger.refresh_display()

except Exception as e:
    #何かしらのエラーをチャッチ
    print(e)
    del __opener
    del __logger
    del __imager
