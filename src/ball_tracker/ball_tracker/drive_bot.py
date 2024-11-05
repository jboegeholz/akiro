import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import struct

class DriveBot(Node):
    def __init__(self):
        super().__init__('drive_bot')

        try:
            self.serial_port = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=9600,
                timeout=1,
                # 8N1
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
        except serial.SerialException:
            self.get_logger().error('Could not open serial port. Using loopback instead.')
            self.serial_port = serial.serial_for_url('loop://', timeout=1)

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.listener_callback,
            10)
        self.get_logger().info('<< Subscribed to /cmd_vel')


    def listener_callback(self, msg):
        self.get_logger().info('Reveived msg from cmd_vel_out')

        linear_x = msg.linear.x
        linear_y = msg.linear.y
        linear_z = msg.linear.z

        angular_x = msg.angular.x
        angular_y = msg.angular.y
        angular_z = msg.angular.z

        self.get_logger().info(
            f'Received cmd_vel - linear: ({linear_x}, {linear_y}, {linear_z}), angular: ({angular_x}, {angular_y}, {angular_z})')

        serial_message = struct.pack('ff', linear_x, angular_z)
        self.serial_port.write(serial_message)
        self.get_logger().info(f'Sent over serial: {serial_message}')
        
    def destroy(self):
        self.serial_port.close()

def main(args=None):
    rclpy.init(args=args)

    drive_bot = DriveBot()
    rclpy.spin(drive_bot)
    drive_bot.destroy()
    drive_bot.destroy_node()
    rclpy.shutdown()