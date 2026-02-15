#include <SoftwareSerial.h>

int32_t left_rpm = 0;
int32_t right_rpm = 0;
SoftwareSerial mySerial(10,11);	// 10-> Rx, 11->Tx  

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
}

void loop() {
  if (mySerial.available() >= 8) {  // 2 Floats à 4 Bytes = 8 Bytes
    
    mySerial.readBytes((char*)&left_rpm, 4);
    mySerial.readBytes((char*)&right_rpm, 4);

    Serial.print("Left RPM: ");
    Serial.println(left_rpm);
    Serial.print("Right RPM: ");
    Serial.println(right_rpm);
  }
}
