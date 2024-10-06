from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            output='screen',
            remappings=[
                ('/cmd_vel', '/cmd_vel_prio')
            ]
        ),
        Node(
            package='twist_mux',
            executable='twist_mux',
            name='twist_mux',
            output='screen',
            parameters=['/akiro/src/ball_tracker/config/twist_mux.yaml']
        )
    ])
