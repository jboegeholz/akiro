from serial.serialutil import SerialException
import serial

def test_pyserial():

    try:
        serial_port = serial.Serial(
            port='/dev/ttyUSB0',  # Passe den Port an
            baudrate=9600,
            timeout=1
        )
    except SerialException as e:
        print(e)

