import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import struct
import math

class DriveBot(Node):
    def __init__(self):
        super().__init__('drive_bot')
        self.wheel_radius = 0.05 #
        self.wheel_base = 0.2
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
            '/cmd_vel_out',
            self.listener_callback,
            10)
        self.get_logger().info('<< Subscribed to /cmd_vel_out')



    def twist_to_rpm(self, linear_x, angular_z):
        v_l = linear_x - angular_z * (self.wheel_base / 2)
        v_r = linear_x + angular_z * (self.wheel_base / 2)

        rpm_l = (v_l / (2 * math.pi * self.wheel_radius)) * 60
        rpm_r = (v_r / (2 * math.pi * self. wheel_radius)) * 60

        return rpm_l, rpm_r

    def listener_callback(self, msg):
        self.get_logger().info('Received msg from cmd_vel_out')

        linear_x = msg.linear.x
        linear_y = msg.linear.y
        linear_z = msg.linear.z

        angular_x = msg.angular.x
        angular_y = msg.angular.y
        angular_z = msg.angular.z

        self.get_logger().info(
            f'Received cmd_vel - linear: ({linear_x}, {linear_y}, {linear_z}), angular: ({angular_x}, {angular_y}, {angular_z})')

        rpm_l, rpm_r = self.twist_to_rpm(linear_x, angular_z)
        serial_message = struct.pack('ii', rpm_l, rpm_r)
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