# converts detected blob keypoints to drive commands
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist


class FollowBall(Node):
    def __init__(self):
        super().__init__('follow_ball')

        self.subscription = self.create_subscription(
            Point,
            '/ball_keypoint',
            self.listener_callback,
            10)
        self.get_logger().info('<< Subscribed to /ball_keypoint')

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def listener_callback(self, msg):
        x = msg.x
        y = msg.y
        size = msg.z
        self.get_logger().info(f"Received keypoint: x: {x} y: {y} size: {size}")
        # convert keypoint to drive command

        self.publisher.publish(Twist(linear=Vector3(x=linear_x), angular=Vector3(z=angular_z)))

def main(args=None):
    rclpy.init(args=args)

    follow_ball = FollowBall()
    rclpy.spin(follow_ball)
    follow_ball.destroy_node()
    rclpy.shutdown()