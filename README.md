# AKIRO - ROS 2 Robot Project

## Lock dependencies

   dpkg-query -W -f='${binary:Package}=${Version}\n' | grep ros- > ros2-packages.lock