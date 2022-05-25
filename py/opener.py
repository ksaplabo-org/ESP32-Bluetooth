import bluetooth
import alert
import time

class Opener():
    """ドアのカギを開錠するクラス"""

    def __init__(self, **env_dict):

        #対象となるESPのMACアドレスとポート番号取得
        self.__mac_addr_esp = env_dict.get("ADDR")
        self.__port_esp = env_dict.get("PORT")

        #接続フラグの初期化
        self.__is_connected = False

        #Bluetooth接続のバッファーカウンタの初期化
        self.__cnt_ble_buffer = 0

        #alertクラスのインスタンス
        self.__bl_err_alert = alert.Alert("LED", "BLUE")

        #Bluetooth接続
        self.__connect_ble(self.__mac_addr_esp, self.__port_esp)

    def __del__(self):
        del self.__bl_err_alert

    def open(self):
        """ドア開錠
        """

        #一度openしてから約7秒過ぎている場合
        if self.__count_connection_interval():

            try:
                #ソケット送信
                self.__ble_socket.send('on')
                print('sendON')
            except Exception:
                print("send Error!")
                self.__connect_ble(self.__mac_addr_esp, self.__port_esp)
                if self.__is_connected:
                    print("Connected!")
                    self.__ble_socket.send('on')

            return True
        return False

    #接続(接続できるまでループする)
    def __connect_ble(self, addr, port):

        try:
            self.__ble_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.__ble_socket.connect((addr, port))

            self.__is_connected = True
            self.__bl_err_alert.stop_alert()
        except Exception:
            print('接続できるESP32がありません')
            self.__is_connected = False
            self.__bl_err_alert.start_alert()

    #約7秒を数えるメソッド(戻り値isSend：Ture→7秒経過、False→7秒未経過)
    def __count_connection_interval(self):

        ret = False

        if self.__cnt_ble_buffer == 0:
            ret = True

        self.__cnt_ble_buffer = self.__cnt_ble_buffer + 1

        if self.__cnt_ble_buffer > 160:
            self.reset_counter()

        return ret

    def reset_counter(self):
        """カウンターリセット
        """
        self.__cnt_ble_buffer = 0
