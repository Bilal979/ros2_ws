from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    ld = LaunchDescription()

    # number_publisher = Node(
    #     package='my_py_pkg',
    #     executable='number_publisher',
    # )
    # number_counter = Node(
    #     package='my_py_pkg',
    #     executable='number_counter',
    # )

    # Adding another launch file
    # other_launch_file = IncludeLaunchDescription(
    #  XMLLaunchDescriptionSource(os.path.join(
    #   get_package_share_directory('my_robot_bringup'),
    #                     'launch/number_app.launch.xml')))


    # Adding parameters from yaml file
    param_config = os.path.join(
        get_package_share_directory("my_robot_bringup"),
        "config", "number_params.yaml")

    # -----------Node renaming and remapping
    number_publisher1 = Node(
        package="my_py_pkg",
        executable="number_publisher",
        name="num_pub1",
        remappings=[("/number", "/my_number")],
        parameters=[{'number': 1}, {'publish_period': 2.0}]
    )
    number_publisher2 = Node(
        package="my_py_pkg",
        executable="number_publisher",
        name="num_pub2",
        remappings=[("/number", "/my_number")],
        # parameters=[{'number': 2}, {'publish_period': 4.0}]
        parameters=[param_config]
    )
    number_counter = Node(
        package="my_py_pkg",
        executable="number_counter",
        remappings=[("/number", "/my_number")]
    )

    ld.add_action(number_publisher1)
    ld.add_action(number_publisher2)
    ld.add_action(number_counter)


    # Adding namespace to node
    # number_publisher_ns = Node(
    #     package='my_py_pkg',
    #     executable='number_publisher',
    #     namespace='/abc'
    # )
    # number_counter_ns = Node(
    #     package='my_py_pkg',
    #     executable='number_counter',
    #     namespace='/abc'
    # )
    
    # ld.add_action(number_publisher_ns)
    # ld.add_action(number_counter_ns)
    # ld.add_action(other_launch_file)
    
    return ld
