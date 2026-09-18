cmake_minimum_required(VERSION 3.8)
project(my_robot_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)


# -------------------Start Interface related things 
find_package(rosidl_default_generators REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME}
  # we will add the name of our custom interfaces here
  "msg/HardwareStatus.msg"
  "srv/ResetCounter.srv"
)
ament_export_dependencies(rosidl_default_runtime)
# ----------------End Interface related things

ament_package()
