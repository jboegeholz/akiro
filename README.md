# AKIRO - ROS 2 Robot Project


## Nodes startenv ia Launchfile

    ros2 launch src/launch/start_robot.launch.py 

## check running nodes

    ros2 node list

## check published topics
    
        ros2 topic list

## Lock dependencies

    dpkg-query -W -f='${binary:Package}=${Version}\n' | grep ros- > ros2-packages.lock

## Range detector

    python range_detector.py --image yellow-tennis-ball.jpg --filter HSV --preview
