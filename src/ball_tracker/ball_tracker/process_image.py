import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')

        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.listener_callback,
            10)
        self.get_logger().info('<< Subscribed to /image_raw')
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        cv_image = None
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.get_logger().info('Receive image data...')
        except CvBridgeError as e:
            self.get_logger().error("CvBridgeError!")
            return

        working_image = cv2.blur(cv_image, (5, 5))
        working_image = cv2.cvtColor(working_image, cv2.COLOR_BGR2HSV)
        thresh_min = (21, 101, 49)
        thresh_max = (145, 255, 255)
        working_image = cv2.inRange(working_image, thresh_min, thresh_max)
        working_image = cv2.dilate(working_image, None, iterations=2)
        working_image = cv2.erode(working_image, None, iterations=2)
        working_image = 255 - working_image

        cv2.imshow("Image Window", working_image)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)

    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)

    image_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
