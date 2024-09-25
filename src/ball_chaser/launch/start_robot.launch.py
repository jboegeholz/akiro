from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Start drive_bot node
        Node(
            package='my_robot_package',
            executable='drive_bot',
            name='drive_bot',
            output='screen'
        ),
        # Start process_image node
        Node(
            package='image_processing_package',
            executable='process_image',
            name='process_image',
            output='screen'
        ),
        # Start v4l2_camera node
        Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
            name='v4l2_camera_node',
            output='screen',
            parameters=[{
                'video_device': '/dev/video0',
                'pixel_format': 'YUYV',
                'image_size': [640, 480]
            }]
        )
    ])
