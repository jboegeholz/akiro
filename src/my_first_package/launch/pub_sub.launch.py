import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    package_dir = get_package_share_directory('my_first_package')
    publisher_launch_path = os.path.join(package_dir, 'launch', 'publisher.launch.py')
    publisher_launch_description = IncludeLaunchDescription(PythonLaunchDescriptionSource(publisher_launch_path))
    ld.add_action(publisher_launch_description)

    subscriber_node = Node(
            package='demo_nodes_py',
            executable='listener',
            name='eary',
            output='screen'
        )

    ld.add_action(subscriber_node)
    return ld