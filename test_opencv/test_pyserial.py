import struct
import pytest
from serial.serialutil import SerialException
import serial

@pytest.mark.mac_os
def test_pyserial_on_mac_os_loopback():
    """
    connect tx and rx to test loopback
    """
    try:
        serial_port = serial.Serial(
            port='/dev/cu.usbserial-1120',  # for mac os
            baudrate=9600,
            timeout=1
        )
    except SerialException as e:
        serial_port = serial.serial_for_url('loop://', timeout=1)

    serial_port.write("asd".encode("utf-8"))
    assert serial_port.readline() == b"asd"

def test_pyserial_struct():
    serial_message = struct.pack('ff', 0.5, 1.0)
    values = struct.unpack('ff',serial_message)
    assert values[0] == 0.5
    assert values[1] == 1.0

@pytest.mark.mac_os
def test_pyserial_on_ubuntu():
    try:
        serial_port = serial.Serial(
            port='/dev/cu.usbserial-10',
            baudrate=9600,
            timeout=1,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
    except SerialException as e:
        serial_port = serial.serial_for_url('loop://', timeout=1)
    serial_message = struct.pack('ii', 0, 0)
    serial_port.write(serial_message)