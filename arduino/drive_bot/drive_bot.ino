#include <DynamixelShield.h>
#include <SoftwareSerial.h>

const uint8_t DXL_ID_1 = 1;
const uint8_t DXL_ID_2 = 2;
const uint32_t BAUDRATE = 57600;
const float DXL_PROTOCOL_VERSION = 2.0;

int32_t left_rpm = 0;
int32_t right_rpm = 0;

DynamixelShield dxl;
SoftwareSerial mySerial(10, 11);  // 10-> Rx, 11->Tx

void setup() {
  mySerial.begin(9600);  // Für Kommando-Empfang
  dxl.begin(BAUDRATE);
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);

  // Init Motor 1
  if (dxl.ping(DXL_ID_1)) {
    dxl.torqueOff(DXL_ID_1);
    dxl.setOperatingMode(DXL_ID_1, OP_VELOCITY);
    dxl.torqueOn(DXL_ID_1);
  }

  // Init Motor 2
  if (dxl.ping(DXL_ID_2)) {
    dxl.torqueOff(DXL_ID_2);
    dxl.setOperatingMode(DXL_ID_2, OP_VELOCITY);
    dxl.torqueOn(DXL_ID_2);
  }
}

void loop() {
  if (mySerial.available() >= 8) {
    mySerial.readBytes((char*)&left_rpm, 4);
    mySerial.readBytes((char*)&right_rpm, 4);

    dxl.setGoalVelocity(DXL_ID_1, left_rpm, UNIT_RPM);
    dxl.setGoalVelocity(DXL_ID_2, right_rpm, UNIT_RPM);
  }
}
