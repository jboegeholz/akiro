from launch import LaunchDescription
from launch.actions import ExecuteProcess


def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=["echo", "Hello from the shell!"],
            output="screen"
        ),
    ])