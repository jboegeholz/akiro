import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher = self.create_publisher(String, 'talker_topic', 10)
        timer_period = 2.0  # Sekunden
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello, from my first ROS 2 publisher node'
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down publisher (Ctrl+C)")
        sys.exit(0)
    finally:
        node.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main()