# AKIRO - ROS 2 Robot Project


## Nodes starten

    ros2 run ball_tracker process_image
    ros2 run v4l2_camera v4l2_camera_node


## check running nodes

    ros2 node list

## Lock dependencies

    dpkg-query -W -f='${binary:Package}=${Version}\n' | grep ros- > ros2-packages.lock

## Range detector

    python range_detector.py --image yellow-tennis-ball.jpg --filter HSV --preview
