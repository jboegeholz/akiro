import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial

class DriveBot(Node):
    def __init__(self):
        super().__init__('cmd_vel_subscriber')

        self.serial_port = serial.Serial(
            port='/dev/ttyUSB0',   # Passe den Port an
            baudrate=9600,
            timeout=1
        )
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

        # TODO send comand to arduino
        serial_message = f"linear: {linear_x}, angular: {angular_z}\n"

        # Sende die Nachricht über die serielle Schnittstelle
        self.serial_port.write(serial_message.encode('utf-8'))
        self.get_logger().info(f'Sent over serial: {serial_message}')
        
    def destroy(self):
        # Schließe die serielle Schnittstelle, wenn der Node zerstört wird
        self.serial_port.close()

def main(args=None):
    rclpy.init(args=args)

    drive_bot = DriveBot()
    rclpy.spin(drive_bot)
    drive_bot.destroy()
    drive_bot.destroy_node()
    rclpy.shutdown()