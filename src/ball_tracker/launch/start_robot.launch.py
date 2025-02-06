from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    process_image_node = Node(
            package='ball_tracker',
            executable='process_image'
         )
    follow_ball_node = Node(
            package='ball_tracker',
            executable='follow_ball'
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
    drive_bot_node = Node(
            package='ball_tracker',
            executable='drive_bot'
         )

    ld.add_action(process_image_node)
    ld.add_action(follow_ball_node)
    ld.add_action(camera_node)
    ld.add_action(drive_bot_node)

    return ld