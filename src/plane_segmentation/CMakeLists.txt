cmake_minimum_required(VERSION 3.8)
project(plane_segmentation)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(pcl_ros REQUIRED)

find_package(PCL REQUIRED)

include_directories(
        include
        ${PCL_INCLUDE_DIRS}
)

add_executable(plane_seg_node src/plane_seg_node.cpp)

ament_target_dependencies(plane_seg_node
        rclcpp
        sensor_msgs
        pcl_conversions
        pcl_ros
)

target_link_libraries(plane_seg_node ${PCL_LIBRARIES})

install(TARGETS
        plane_seg_node
        DESTINATION lib/${PROJECT_NAME}
)
ament_package()




