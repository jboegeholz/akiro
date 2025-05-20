import time
import unittest
import launch
import launch_ros
import launch_testing.actions
import rclpy
import pytest
from std_msgs.msg import String


@pytest.mark.launch_test
def generate_test_description():
    return (
        launch.LaunchDescription(
            [
                # Nodes under test
                launch_ros.actions.Node(
                    package='my_first_package',
                    namespace='',
                    executable='talker',
                    name='talker1',
                ),
                # Launch tests 0.5 s later
                launch.actions.TimerAction(
                    period=0.5, actions=[launch_testing.actions.ReadyToTest()]),
            ]
        ), {},
    )


class TestTalkerNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()

    def setUp(self):
        self.node = rclpy.create_node('test_talker_node')

    def tearDown(self):
        self.node.destroy_node()

    def test_publishes_messages(self, proc_output):
        msgs_rx = []
        sub = self.node.create_subscription(
            String, 'talker_topic',
            lambda msg: msgs_rx.append(msg), 100)
        try:
            end_time = time.time() + 10
            while time.time() < end_time:
                rclpy.spin_once(self.node, timeout_sec=1)
            assert msgs_rx
        finally:
            self.node.destroy_subscription(sub)

    def test_logs_spawning(self, proc_output):
        proc_output.assertWaitFor(
            'Publishing: "Hello, from my first ROS 2 publisher node"',
            timeout=5, stream='stderr')

@launch_testing.post_shutdown_test()
class TestTalkerNodeShutdown(unittest.TestCase):
    def test_exit_codes(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)