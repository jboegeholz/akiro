#include <DynamixelShield.h> 
const uint8_t DXL_ID_1 = 1;
const uint8_t DXL_ID_2 = 2;
const uint32_t BAUDRATE = 57600; 
const float DXL_PROTOCOL_VERSION = 2.0; 

DynamixelShield dxl; 

void setup() { 
  dxl.begin(BAUDRATE); 
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION); 

  if(dxl.ping(DXL_ID_1) == true){ 
    dxl.torqueOff(DXL_ID_1); 
    dxl.setOperatingMode(DXL_ID_1, OP_VELOCITY); 
    dxl.torqueOn(DXL_ID_1);   
  } 
  
  if (dxl.ping(DXL_ID_2)) {
    dxl.torqueOff(DXL_ID_2);
    dxl.setOperatingMode(DXL_ID_2, OP_VELOCITY);
    dxl.torqueOn(DXL_ID_2);
  }

} 

void loop() { 
  dxl.setGoalVelocity(DXL_ID_1, 200.0, UNIT_RAW); 
  dxl.setGoalVelocity(DXL_ID_2, 200.0, UNIT_RAW); 
  delay(3000); 
  dxl.setGoalVelocity(DXL_ID_1, 0.0, UNIT_RAW); 
  dxl.setGoalVelocity(DXL_ID_2, 0.0, UNIT_RAW); 
  delay(3000); 
  dxl.setGoalVelocity(DXL_ID_1, -200.0, UNIT_RAW); 
  dxl.setGoalVelocity(DXL_ID_2, -200.0, UNIT_RAW); 
  delay(3000); 
  dxl.setGoalVelocity(DXL_ID_1, 0.0, UNIT_RAW); 
  dxl.setGoalVelocity(DXL_ID_2, 0.0, UNIT_RAW); 
  delay(3000); 
}