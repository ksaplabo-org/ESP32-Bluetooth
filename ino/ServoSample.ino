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
