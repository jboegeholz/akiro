from launch import LaunchDescription, logging

def generate_launch_description():
    ld = LaunchDescription()
    logger = logging.get_logger(__name__)
    logger.info(f"Hello from {__name__}")
    return ld