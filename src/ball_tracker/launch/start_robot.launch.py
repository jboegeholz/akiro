from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    detect_node = Node(
            package='ball_tracker',
            executable='process_image'
         )
    camera_node = Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
            name='v4l2_camera_node',
            output='screen',
            parameters=[{
                'video_device': '/dev/video0',
                'time_per_frame': [1, 6],
                'pixel_format': 'YUYV',
                'image_size': [640, 480]
            }]
        )
    return LaunchDescription([
        detect_node,
        camera_node

    ])
