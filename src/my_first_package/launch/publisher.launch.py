from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    publisher_node = Node(
            package='demo_nodes_py',
            executable='talker',
            output='screen'
        )
    ld.add_action(publisher_node)
    return ld