import struct

from serial.serialutil import SerialException
import serial

def test_pyserial_on_mac_os():
    try:
        serial_port = serial.Serial(
            port='/dev/cu.usbserial-110',  # for mac os
            baudrate=9600,
            timeout=1
        )
    except SerialException as e:
        serial_port = serial.serial_for_url('loop://', timeout=1)

    serial_port.write("asd".encode("utf-8"))
    assert serial_port.readline() == b"asd"

def test_pyserial_struct():
    try:
        serial_port = serial.Serial(
            port='/dev/cu.usbserial-110',  # for mac os
            baudrate=9600,
            timeout=1
        )
    except SerialException as e:
        serial_port = serial.serial_for_url('loop://', timeout=1)
    serial_message = struct.pack('ff', 0.5, 1.0)
    serial_port.write(serial_message)
    values = struct.unpack('ff',serial_port.readline())
    assert values[0] == 0.5
    assert values[1] == 1.0