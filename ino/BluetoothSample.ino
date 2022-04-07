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
