from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
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

    process_image_node = Node(
        package='ball_tracker',
        executable='process_image'
    )

    ld.add_action(camera_node)
    ld.add_action(process_image_node)

    return ld
