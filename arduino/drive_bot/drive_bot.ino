#include <DynamixelShield.h> 
#include <SoftwareSerial.h>

const uint8_t DXL_ID_1 = 1; 
const uint8_t DXL_ID_2 = 2; 
const uint32_t BAUDRATE = 57600; 
const float DXL_PROTOCOL_VERSION = 2.0; 
float linear_velocity = 0.0;
float angular_velocity = 0.0;
float wheel_base = 0.3;
DynamixelShield dxl; void 
SoftwareSerial mySerial(10,11);	// 10-> Rx, 11->Tx  

setup() { 
  mySerial.begin(9600,SERIAL_8N2);
  dxl.begin(BAUDRATE); 
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION); 

  if(dxl.ping(DXL_ID_1) == true){ 
    dxl.torqueOff(DXL_ID_1); 
    dxl.setOperatingMode(DXL_ID_1, OP_VELOCITY); 
    dxl.torqueOn(DXL_ID_1); 
    dxl.setGoalVelocity(DXL_ID_1, 50, UNIT_RPM); 
  } 
  
  if(dxl.ping(DXL_ID_2) == true){ 
    dxl.torqueOff(DXL_ID_2); 
    dxl.setOperatingMode(DXL_ID_2, OP_VELOCITY); 
    dxl.torqueOn(DXL_ID_2); 
    dxl.setGoalVelocity(DXL_ID_2, 50, UNIT_RPM); 
  } 
} 

void loop() { 
  if (mySerial.available()) {
    byte buffer[8];
    mySerial.readBytes(buffer, 8);

    memcpy(&linear_x, &buffer[0], 4);
    memcpy(&angular_z, &buffer[4], 4);
    float v_left = linear_velocity - (angular_velocity * wheel_base / 2);
    float v_right = linear_velocity + (angular_velocity * wheel_base / 2);
  }
    dxl.setGoalVelocity(DXL_ID_1, v_left, UNIT_RPM);
    dxl.setGoalVelocity(DXL_ID_2, v_right, UNIT_RPM);
}