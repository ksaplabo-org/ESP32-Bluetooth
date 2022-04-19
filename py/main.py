#処理はなるべく止めないように
import time
import logger           #ログ登録クラス
import opener           #ドア開錠クラス
import imager           #画像解析クラス

#各クラスのインスタンス生成                        
_logger = logger.Logger()
_opener = opener.Opener(addr='78:21:84:80:2f:aa',port=1)
_imager = imager.ImgAnalysis()

try:
    #リアルタイム静止画像の読み取りを繰り返す
    while(True):

        #顔認証行う
        try:
            result = _imager.img_analysis()
        except:
            #異常終了の場合
            print('CameraErr')
            time.sleep(1)

            #インスタンスを削除し、再生成
            del _imager
            _imager = imager.ImgAnalysis()
            
            continue
        
        #顔認識した場合
        if result == True:
            #print("顔認識OK")
            #ドアOpen
            if _opener.open():
                #Openした時のログを保持
                _logger.write()

        #顔認証してない場合
        else:
            #print("顔認証NG")
            #初期化
            _opener.reset()
except:
    del _opener
    del _logger
    del _imager