#include <SoftwareSerial.h>

float linear_x = 0.0;
float angular_z = 0.0;
SoftwareSerial mySerial(10,11);	// 10-> Rx, 11->Tx  
void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
}

void loop() {
  if (mySerial.available() >= 8) {  // 2 Floats à 4 Bytes = 8 Bytes
    byte buffer[8];
    mySerial.readBytes(buffer, 8);

    memcpy(&linear_x, &buffer[0], 4);
    memcpy(&angular_z, &buffer[4], 4);

    Serial.print("Linear X: ");
    Serial.println(linear_x);
    Serial.print("Angular Z: ");
    Serial.println(angular_z);
  }
}
