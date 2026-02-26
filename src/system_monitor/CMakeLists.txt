cmake_minimum_required(VERSION 3.8)
project(system_monitor)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(akiro_interfaces REQUIRED)


add_executable(system_monitor_node src/system_monitor_node.cpp)
ament_target_dependencies(system_monitor_node rclcpp akiro_interfaces)

install(TARGETS
        system_monitor_node
        DESTINATION lib/${PROJECT_NAME}
)

ament_package()
