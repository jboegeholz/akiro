from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'ball_tracker'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['tests']),
    data_files=[
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('lib/' + package_name, [package_name + '/blob_detector.py']), # to avoid importing module via package name
        ('lib/' + package_name, [package_name + '/drive_bot.py']), # to avoid importing module via package name
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jboegeholz',
    maintainer_email='jboegeholz@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'process_image = ball_tracker.process_image:main',
            'follow_ball = ball_tracker.follow_ball:main',
            'drive_bot = ball_tracker.drive_bot:main'
        ],
    },
)
