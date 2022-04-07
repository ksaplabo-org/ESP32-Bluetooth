#include "BluetoothSerial.h"
#include <Servo.h>
#include <string.h>

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

    // シリアルモニタに受け取ったデータを表示
    Serial.println(readBuf);
    readBuf = readBuf.substring(0,2);

    if (readBuf.startsWith("on") && !isOpen){
      Open();
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
  delay(20);
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