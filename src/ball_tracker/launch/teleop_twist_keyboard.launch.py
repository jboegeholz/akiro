from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Hole den Paketpfad
    package_path = get_package_share_directory('ball_tracker')

    # Erstelle den vollständigen Pfad zur Konfigurationsdatei
    config_file_path = os.path.join(package_path, 'config', 'config.yaml')
    
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
            parameters=[config_file_path]

        )
    ])
