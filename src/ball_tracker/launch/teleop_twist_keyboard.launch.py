from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    package_path = get_package_share_directory('ball_tracker')

    twist_mux_config_file_path = os.path.join(package_path, 'config', 'twist_mux.yaml')
    twist_joy_config_file_path = os.path.join(package_path, 'config', 'twist_joy.yaml')
    teleop_twist_key = Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            output='screen',
            remappings=[
                ('/cmd_vel', '/cmd_vel_sec')
            ]
        )
    teleop_twist_joy = Node(
            package='teleop_twist_joy',
            executable='teleop_twist_joy',
            output='screen',
            remappings=[
                ('/cmd_vel', '/cmd_vel_prio')
            ],
            parameters=[twist_joy_config_file_path]
        )
    twist_mux = Node(
            package='twist_mux',
            executable='twist_mux',
            name='twist_mux',
            output='screen',
            parameters=[twist_mux_config_file_path]
        )
    return LaunchDescription([
        teleop_twist_key,
        teleop_twist_joy,
        twist_mux
    ])
