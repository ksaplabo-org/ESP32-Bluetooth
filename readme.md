# ESP32にBluetooth接続しServoを動かす  
## 目次  
- [目的説明](#content1)  
- [配線接続](#content2)  
- [ESP32からServoを動かす](#content3)  
- [Raspberry PiにOpencvをインストール](#content4)
- [PythonでBluetooth通信](#content5)  
- [Raspberry Piとカメラを使って顔検出](#content6)  
- [顔認識でServoを動かす](#content7)  

<h2 id="content1">目的説明</h2>  

事務所から外へ出るときの紐を自動で引っ張る仕組みを実装する。  
   
ドア付近に設置するカメラが顔を認識。  
↓  
顔を認識したことをRasPiからESP32へ知らせる。  
↓  
ESP32のプログラムが実行され、紐とつながったモータ(Servo)を動かす  

<h2 id="content2">配線接続</h2>  

- 下図のようにESP32とServoを配線を接続する。  
  ※ここでServoから出ている黄色い線は、ESP32の「D27」につなぐこと。
  　(「D27」に指定している理由は、この後のソースをそのまま使用するため。)
<img alt="OSインストーラ画像" src="./img/servo.png" width="500" height="350">   

<h2 id="content3">ESP32からServoを動かす</h2>  

- ESP32を動かすためのIDEをインストールする。  
<img alt="OSインストーラ画像" src="./img/スクリーンショット 2022-04-01 101506.png" width="700" height="400">   

- 環境設定の説明 ～一度自分でやってみないとわからない～  
  
  起動したら以下の設定を行う。  

  - ボードマネージャURLの追加  
    URL →　[https://dl.espressif.com/dl/package_esp32_index.json]  
    ファイル > 環境設定  
    を開き、ボードマネージャーを追加します。  
    <img alt="OSインストーラ画像" src="./img/スクリーンショット 2022-04-05 100508.png" width="700" height="400">   

  - ボードマネージャインストール  
    ツール  > ボード > ボードマネージャ...  
    を開き  
    <img alt="OSインストーラ画像" src="./img/スクリーンショット 2022-04-05 102011.png" width="700" height="400">   
    
    検索欄にESPを入力し、インストールする。  
    <img alt="OSインストーラ画像" src="./img/スクリーンショット-2021-08-01-140620.png" width="700" height="400">   
  
  -  ボードを選択  
    ツール  > ボード > ESP32 Arduino > ESP32 Dev Module    
    <img alt="OSインストーラ画像" src="./img/スクリーンショット-2021-08-01-140921-1024x690.png" width="700" height="400">   
    
- 動作確認  

  以下のソースをArduinoIDEにコピー。  

  ```C#  
  #include <Servo.h>

  Servo myservo; //Servoオブジェクトを作成

  void setup() {
    myservo.attach(27); //27番ピンにサーボ制御線（黄色）を接続
  }

  void loop() {
    myservo.write(180); //180度へ回転 
    delay(1000);
    myservo.write(0); //元に戻る
    delay(1000);
  }
  ```  

  Servoが動いたらOK。

<h2 id="content4">Raspberry PiにOpencvをインストール</h2>  

- Raspberry Piの設定手順はこちらを参考→https://github.com/ksaplabo-org/Raspi-Setup  

- Tera Termを起動して、以下のコマンドを実行する。  
  ```  
  mkdir Opencv
  cd Opencv

  sudo nano OpencvInstall.sh
  ```  

  以下のソースを貼り付ける。
  ```  sh
  # パッケージ管理ツールの更新（apt-getでインストールをするときは必ず行います。）
  sudo apt-get -y update
  sudo apt-get -y upgrade

  # Githubのページを参考にライブラリをダウンロード
  # 開発ツール
  sudo apt-get -yV install build-essential
  sudo apt-get -yV install cmake
  # 行列演算
  sudo apt-get -yV install libeigen3-dev
  # GUIフレームワーク関連
  sudo apt-get -yV install libgtk-3-dev
  sudo apt-get -yV install qt5-default
  sudo apt-get -yV install libvtk7-qt-dev
  sudo apt-get -yV install freeglut3-dev
  # 並列処理関連
  sudo apt-get -yV install libtbb-dev
  # 画像フォーマット関連
  sudo apt-get -yV install libjpeg-dev
  sudo apt-get -yV install libopenjp2-7-dev
  sudo apt-get -yV install libpng++-dev
  sudo apt-get -yV install libtiff-dev
  sudo apt-get -yV install libopenexr-dev
  sudo apt-get -yV install libwebp-dev
  # 動画像関連
  sudo apt-get -yV install libavresample-dev
  # その他
  sudo apt-get -yV install libhdf5-dev
  # Python関連
  sudo apt-get -yV install libpython3-dev
  sudo apt-get -yV install python3-numpy python3-scipy python3-matplotlib

  # gitのインストール（ソースをダウンロードするときに使います。）
  sudo apt-get -y install git

  # ソースのダウンロード
  cd /usr/local
  sudo mkdir opencv4
  cd /usr/local/opencv4
  sudo git clone https://github.com/opencv/opencv.git
  sudo git clone https://github.com/opencv/opencv_contrib.git

  # ビルド用のディレクトリ作成（buildディレクトリを作成してその中でビルドするのがお作法です。）
  cd opencv
  sudo mkdir build
  cd build

  # ビルド
  # 基本的にはOpenCV公式ページを参考にしました。
  sudo cmake \
  -D CMAKE_BUILD_TYPE=Release \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D OPENCV_EXTRA_MODULES_PATH=/usr/local/opencv4/opencv_contrib/modules \
  PYTHON3_EXECUTABLE=/usr/lib/python3.7 \
  PYTHON_INCLUDE_DIR=/usr/include/python3.7 \
  PYTHON_INCLUDE_DIR2=/usr/include/arm-linux-gnueabihf/python3.7m \
  PYTHON_LIBRARY=/usr/lib/arm-linux-gnueabihf/libpython3.7m.so \
  PYTHON3_NUMPY_INCLUDE_DIRS =/usr/lib/python3/dist-packages/numpy/core/include \
  -S /usr/local/opencv4/opencv

  sudo make -j7
  sudo make install
  ``` 
  
- shファイルの実行はデフォルトで権限がないため、以下のコマンドを実行する。  
  ```  
  sudo chmod 777 OpencvInstall.sh
  ```  
  shファイルを実行  
  ```  
  OpencvInstall.sh
  ```  

- 動作確認  
  以下のコマンドを実行  
  ```  
  python3
  ```  
  
  ```  
  import cv2
  ```

  これでエラーが出なければインストール成功。  

- 動作確認でエラーが出る場合  
  上記のimport cv2を実行すると以下のエラーが出る。  
  <エラー画像挿入>  

  上図のエラー内容は、Opencvを使うためのパッケージが存在しないせいでおこるエラーで
  このようなエラーが出た場合は、以下のサイトを参考にパッケージのインストールを行う。  

  <参考サイト>  
  https://www.shangtian.tokyo/entry/2020/01/02/103124?msclkid=3cbfef7fb3bd11eca1390dff498f0039  
  numpyのパッケージのインストールはこのサイト  
  https://algorithm.joho.info/programming/python/numpy-core-multiarray-failed-to-import/?msclkid=871cc269b3be11ecbea8b1672457fdd1   

<h2 id="content5">PythonでBluetooth通信</h2>  

- pythonでServoを動かす。

  Opencvフォルダ下で以下のファイルを作成する。

  ```  
  sudo nano blcontroll.py
  ``` 

  以下のソースをコピー  
  ※このソースは現在検討中、いったんこれで動く

  ```  
  import bluetooth

  server_addr = 'ESP32のMACアドレス'
  server_port = 1

  sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
  sock.connect((server_addr, server_port))

  sock.send('on')
  ```  

  ESP32とPCを接続し、Arduino IDEを開き、以下のソースをコピー  
   
  ```C#  
  #include <Servo.h>
  #include "BluetoothSerial.h"

  #if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
  #error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
  #endif

  #define BT_NAME "Servo"

  BluetoothSerial SerialBT;
  Servo myservo; //Servoオブジェクトを作成

  void setup() {
    myservo.attach(27); //27番ピンにサーボ制御線（黄色）を接続
    SerialBT.begin(BT_NAME); 
    Init();
  }

  void loop() {
    String readBuf="";
    
    if (SerialBT.available()) {
      
      // BlueToothからデータ読み込み
      readBuf = SerialBT.readString();

      if (readBuf.startsWith("on")){
        Open();
      }
    }
  }

  void Open(){
  for (int pos = 180; pos >= 0; pos -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(3);                       // waits 15ms for the servo to reach the position
    }
  }
  void Init(){
    myservo.write(180);
    delay(5);
  }

  ```  

  以下のコマンドでソースを実行  

  ```  
  python3 blcontroll.py
  ```  

  servoモータが動けばOK。  

<h2 id="content6">Raspberry Piとカメラを使って顔検出</h2>  

- 外部カメラとRaspberry Piを接続する。
- 顔検出のサンプルコードを作成する。  

　Opencvフォルダ下で以下のファイルを作成する。  

  ```  
  sudo nano sample.py
  ```  

  以下のソースをコピー  
  (0.1秒毎に画像から顔を認識し、「顔認識OK」か「顔認識NG」をterminal上に出力するプログラム)  

  ```python  
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
  ```  

- 動作確認  
  以下のコマンドでソースを実行  
  ```
  python3 sample.py  
  ```

  下図のような実行結果になればOK  

  <img alt="OSインストーラ画像" src="./img/スクリーンショット 2022-04-05 135741.png" width="700" height="400">  

<h2 id="content7">顔認識でServoを動かす</h2>  

- ESP32とPCを接続し、Arduino IDEを開き、以下のソースをコピー  

```C#  
#include "BluetoothSerial.h"
#include <Servo.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#define BT_NAME "Servo"

BluetoothSerial SerialBT;
Servo myservo;

bool isOpen=false;
int count = 0;

void setup() {
  Serial.begin(115200);
  SerialBT.begin(BT_NAME);  
  myservo.attach(27);
  Init();
}

void loop() {
  String readBuf="";
  
  if (SerialBT.available()) {
    
    // BlueToothからデータ読み込み
    readBuf = SerialBT.readString();

    Serial.println(readBuf);

    if (readBuf.startsWith("on") && !isOpen){
      Open();
    }
    if (readBuf.startsWith("off") && isOpen){
      Close();
    }
  }
  if (isOpen){
    count = count + 1;
  } else {
    count = 0;
  }
  if(count > 50){
    Close();
    count=0;
  }
  delay(30);
}  
void Open(){
  for (int pos = 180; pos >= 0; pos -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(3);                       // waits 15ms for the servo to reach the position
  }
  isOpen = true;
}
void Close(){
  for (int pos = 0; pos <= 180; pos += 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(3);                       // waits 15ms for the servo to reach the position
  }
  isOpen = false;
}
void Init(){
  myservo.write(180);
  delay(5);
}

```  

- Opencvフォルダ下で以下のファイルを作成する。  

```  
sudo nano Opencv.py
```  

以下のソースをコピー  
(ソースは検討中)  

```python  
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

```  

- pythonを実行して動作確認