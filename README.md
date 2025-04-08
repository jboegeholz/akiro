# AKIRO - ROS 2 Robot Project
    
## Check camera status

    v4l2-ctl --list-devices

## Start nodes via launchfile

    ros2 launch src/launch/start_robot.launch.py 

## check running nodes

    ros2 node list

## check published topics
    
    ros2 topic list

## Lock dependencies

    dpkg-query -W -f='${binary:Package}=${Version}\n' | grep ros- > ros2-packages.lock

## Range detector

    python3 range_detector.py --image tennis-ball.jpg --filter HSV --preview
