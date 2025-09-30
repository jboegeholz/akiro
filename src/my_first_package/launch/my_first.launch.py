from launch import LaunchDescription
import launch

def generate_launch_description():
    ld = LaunchDescription()
    logger = launch.logging.get_logger(__name__)
    logger.info(f"Hello from {__name__}")
    return ld