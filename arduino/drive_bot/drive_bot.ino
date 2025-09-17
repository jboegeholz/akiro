#include <DynamixelShield.h>
#include <SoftwareSerial.h>

const uint8_t DXL_ID_1 = 1;
const uint8_t DXL_ID_2 = 2;
const uint32_t BAUDRATE = 57600;
const float DXL_PROTOCOL_VERSION = 2.0;
const float wheel_base = 0.3;

float linear_velocity = 0.0;
float angular_velocity = 0.0;

float v_left = 0.0;
float v_right = 0.0;

DynamixelShield dxl;
SoftwareSerial mySerial(10, 11);  // Rx, Tx (für externe Befehle)

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
    byte buffer[8];
    mySerial.readBytes(buffer, 8);

    memcpy(&linear_velocity, &buffer[0], 4);
    memcpy(&angular_velocity, &buffer[4], 4);

    v_left  = linear_velocity - (angular_velocity * wheel_base / 2.0);
    v_right = linear_velocity + (angular_velocity * wheel_base / 2.0);

    // Setze Geschwindigkeit
    dxl.setGoalVelocity(DXL_ID_1, v_left, UNIT_RPM);
    dxl.setGoalVelocity(DXL_ID_2, v_right, UNIT_RPM);
  }
}
