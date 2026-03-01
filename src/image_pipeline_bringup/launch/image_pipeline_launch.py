from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    kinect_node = Node(
        package='kinect_ros2',
        executable='kinect_ros2_node',
        name='kinect_node',
        output='screen'
    )

    voxel_node = Node(
        package='voxel_filter',
        executable='voxel_node',
        name='voxel_filter_node',
        output='screen',
        parameters=[
            {'leaf_size': 0.005}
        ]
    )

    plane_node = Node(
        package='plane_segmentation',
        executable='plane_seg_node',
        name='plane_segmentation_node',
        output='screen',
    )

    return LaunchDescription([
        kinect_node,
        voxel_node,
        plane_node
    ])
