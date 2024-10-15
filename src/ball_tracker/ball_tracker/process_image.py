import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
from geometry_msgs.msg import Point
from blob_detector import BlobDetector


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
        self.blob_detector = BlobDetector()

        self.publisher = self.create_publisher(Point, '/ball_keypoint', 10)

    def listener_callback(self, msg):
        try:
            image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.get_logger().info('Receive image data...')
        except CvBridgeError as e:
            self.get_logger().error("CvBridgeError!")
            return

        keypoints, working_image = self.blob_detector.detect_blob(image)
        if keypoints:
            self.get_logger().info(f"Got keypoint: x: {keypoints[0].pt[0]} y: {keypoints[0].pt[1]} size: {keypoints[0].size}")
            # determine biggest keypoint
            biggest_keypoint = keypoints[0]
            for keypoint in keypoints:
                if keypoint.size > biggest_keypoint.size:
                    biggest_keypoint = keypoint
            self.publisher.publish(Point(x=biggest_keypoint.pt[0], y=biggest_keypoint.pt[1], z=biggest_keypoint.size))

        image_with_keypoints = cv2.drawKeypoints(working_image, keypoints, np.array([]), (0, 0, 255),
                                                 cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow("Keypoints", image_with_keypoints)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)

    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)

    image_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
