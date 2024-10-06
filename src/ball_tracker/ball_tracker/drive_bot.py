import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DriveBot(Node):
    def __init__(self):
        super().__init__('cmd_vel_subscriber')

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

        # TODO send comand via rosserial to arduino


def main(args=None):
    rclpy.init(args=args)

    drive_bot = DriveBot()
    rclpy.spin(drive_bot)

    drive_bot.destroy_node()
    rclpy.shutdown()