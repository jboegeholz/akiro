# AKIRO - ROS 2 Robot Project

## check running nodes

    ros2 node list

## Lock dependencies

    dpkg-query -W -f='${binary:Package}=${Version}\n' | grep ros- > ros2-packages.lock

