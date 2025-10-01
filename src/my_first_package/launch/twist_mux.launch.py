from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ld = LaunchDescription()

    package_path = get_package_share_directory('my_first_package')
    twist_mux_config_file_path = os.path.join(package_path, 'config', 'twist_mux.yaml')

    twist_mux = Node(
            package='twist_mux',
            executable='twist_mux',
            name='twist_mux',
            output='screen',
            parameters=[twist_mux_config_file_path]
        )

    ld.add_action(twist_mux)
    return ld