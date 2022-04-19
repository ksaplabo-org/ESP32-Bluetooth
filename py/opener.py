import bluetooth
import alert
import time

class Opener():

    is_send = True
    cnt = 0
    
    global addr
    global port
    global bl_err_alert
    global btsocket

    def __init__(self, **env_dict):

        self.addr = env_dict.get("addr")
        self.port = env_dict.get("port")
        #alertクラスのインスタンス
        self.bl_err_alert = alert.Alert("LED", "BLUE")

        #Bluetooth接続
        self.__connect(self.addr, self.port)

    def __del__(self):
        del self.bl_err_alert

    #ドア開錠
    def open(self):
        
        #一度openしてから約7秒過ぎている場合
        if self.count_check():

            try:
                #ソケット送信
                self.btsocket.send('on')
                print('sendON')
            except:    
                print("send Error!")
                self.__connect(self.addr, self.port)
                if not (self.btsocket == None):
                    print("disConnected!")
                    self.btsocket.send('on')
            
            #Bluetooth切断
            #self.__disconnect(btsocket)

            return True
        return False

    #接続(接続できるまでループする)
    def __connect(self, addr, port):
        
        try:
            self.btsocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.btsocket.connect((addr, port))
            
            self.bl_err_alert.stop()
        except :
            print('接続できるESP32がありません')
            self.bl_err_alert.start()

    #切断
    #def __disconnect(self, sock):
        #sock.close()

    #約7秒を数えるメソッド(戻り値isSend：Ture→7秒経過、False→7秒未経過)
    def count_check(self):

        ret = False

        if self.cnt == 0:
            ret = True
        
        self.cnt = self.cnt + 1

        if self.cnt > 160:
            self.reset()

        return ret

    #カウンターリセット
    def reset(self):
        self.cnt = 0
