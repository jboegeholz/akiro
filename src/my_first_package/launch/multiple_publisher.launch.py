from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    publisher_node_1 = Node(
            package='demo_nodes_py',
            executable='talker',
            name='noisy',
            output='screen'
        )
    publisher_node_2 = Node(
            package='demo_nodes_py',
            executable='talker',
            name='rowdy',
            output='screen'
        )
    ld.add_action(publisher_node_1)
    ld.add_action(publisher_node_2)
    return ld