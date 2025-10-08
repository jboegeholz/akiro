from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ld = LaunchDescription()
    package_path = get_package_share_directory('ball_tracker')

    twist_joy_config_file_path = os.path.join(package_path, 'config', 'twist_joy_ps3.yaml')

    joy_node = Node(
            package='joy',
            executable='joy_node',
            name='joy_node',
            output='screen'
        )
    teleop_twist_joy = Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            output='screen',
            remappings=[
                ('/cmd_vel', '/turtle1/cmd_vel')
            ],
            parameters=[twist_joy_config_file_path]
        )

    #ros2 run turtlesim turtlesim_node
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node'
    )
    ld.add_action(joy_node)
    ld.add_action(teleop_twist_joy)
    ld.add_action(turtlesim_node)
    return ld
