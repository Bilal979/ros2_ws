# ROS 2 Workspace

This workspace brings together small ROS 2 applications that demonstrate how nodes communicate through topics, services, and actions. It also includes a parameterized mobile-robot description, launch files for running the applications, and a sample rosbag.

The examples use Python (`rclpy`) and ROS 2 interfaces. The included bag metadata identifies ROS 2 Jazzy; the packages are built with `colcon`.

## What’s in the workspace

| Package or resource | Purpose |
| --- | --- |
| [`my_py_pkg`](src/my_py_pkg/) | Python nodes for publishing and accumulating numbers, resetting the counter, and demonstrating action clients and servers. |
| [`my_robot_interfaces`](src/my_robot_interfaces/) | Custom ROS interfaces: `HardwareStatus`, `ResetCounter`, `ActivateTurtle`, and `CountUntil`. |
| [`turtle_controller`](src/turtle_controller/) | A parameterized turtlesim controller with a service to activate or deactivate controller updates. |
| [`my_robot_bringup`](src/my_robot_bringup/) | Launch files and YAML parameters for the number and turtlesim applications. |
| Robot description files | A mobile-base model in URDF and Xacro, with reusable dimensions and materials. These files are at the workspace root and are not part of the launch package. |
| [`bags/bag1`](bags/bag1/) | A sample MCAP rosbag containing messages on the `/number` topic. |

### Directory layout

```text
.
├── bags/
│   └── bag1/                       # Sample MCAP recording and metadata
├── common_properties.xacro         # Shared robot materials
├── mobile_base.xacro               # Parameterized mobile-base links and joints
├── my_robot.urdf                   # Expanded robot description
├── my_robot.urdf.xacro             # Xacro entry point for the robot model
└── src/
    ├── my_py_pkg/                  # Number, service, and action examples
    ├── my_robot_bringup/           # Launch files and parameter YAML
    ├── my_robot_interfaces/        # Custom message, service, and action definitions
    └── turtle_controller/          # Turtlesim controller node
```

## Requirements

- ROS 2 (Jazzy is the distribution identified in the included rosbag metadata)
- `colcon` and the ROS dependencies declared by the packages, including `rclpy`, `turtlesim`, `geometry_msgs`, and `example_interfaces`
- `ros2 bag` / MCAP support to inspect or play the included recording
- The `xacro` package to expand the robot description

Install any missing package dependencies with `rosdep` from the workspace root:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

## Build and source

In a terminal with ROS 2 installed, replace `<ros-distro>` with your installed distribution:

```bash
source /opt/ros/<ros-distro>/setup.bash
cd /path/to/ros2_ws
colcon build --symlink-install
source install/local_setup.bash
```

Source the ROS installation and `install/local_setup.bash` in each new terminal before running the examples.

## Run the applications

### Number publishers and counter

Start the number application with either launch description:

```bash
ros2 launch my_robot_bringup number_app.launch.py
# Or use the XML launch description:
ros2 launch my_robot_bringup number_app.launch.xml
```

Each launch starts two number publishers and a counter. The publishers are remapped from `/number` to `/my_number`; the counter adds each received value to its running total. The launch files configure publisher values and periods using node parameters and `config/number_params.yaml`.

In another sourced terminal, inspect the combined topic or reset the counter:

```bash
ros2 topic echo /my_number
ros2 service call /reset_counter my_robot_interfaces/srv/ResetCounter "{reset_value: 0}"
```

The reset request is accepted only when its value is non-negative and no greater than the current total.

### Turtlesim controller

```bash
ros2 launch my_robot_bringup turtle_app.launch.xml
```

This starts two turtlesim/controller pairs in the `/t1` and `/t2` namespaces. The controller parameters give each pair a different background, pen colors, and movement speed. Each controller changes its velocity based on the turtle’s horizontal position and changes the pen color when it crosses the configured region.

The `activate_turtle` service enables or suppresses controller updates for the corresponding turtle:

```bash
ros2 service call /t1/activate_turtle my_robot_interfaces/srv/ActivateTurtle "{activate: false}"
ros2 service call /t1/activate_turtle my_robot_interfaces/srv/ActivateTurtle "{activate: true}"
```

### Count-until action

The action server and clients are available as separate executables. Start the server:

```bash
ros2 run my_py_pkg count_until_server
```

Then send a goal from another sourced terminal:

```bash
ros2 action send_goal /count_until my_robot_interfaces/action/CountUntil \
  "{target_number: 5, delay: 0.5}" --feedback
```

The goal requests a target number and delay; the server publishes progress and returns the number reached. The full server supports cancellation. Minimal client/server variants are also included for comparison.

### Individual nodes

The Python package also provides standalone executables:

```bash
ros2 run my_py_pkg test_node
ros2 run my_py_pkg number_publisher
ros2 run my_py_pkg number_counter
ros2 run my_py_pkg reset_counter_client
```

`number_publisher` publishes to `/number` by default and accepts `number` and `publish_period` parameters. For example:

```bash
ros2 run my_py_pkg number_publisher --ros-args -p number:=4 -p publish_period:=1.0
```

The counter and reset client require the corresponding ROS nodes and custom interfaces to be available.

## Robot description

[`my_robot.urdf.xacro`](my_robot.urdf.xacro) includes [`common_properties.xacro`](common_properties.xacro) and [`mobile_base.xacro`](mobile_base.xacro). The model describes a box-shaped base, two continuous-joint wheels, a fixed caster, and a base footprint. [`my_robot.urdf`](my_robot.urdf) is a standalone URDF version of the model.

To expand the Xacro file from the workspace root:

```bash
ros2 run xacro xacro my_robot.urdf.xacro -o /tmp/my_robot.urdf
```

The robot description is provided as model files; no robot hardware driver or robot-specific bringup launch is included.

## Sample rosbag

The recording in `bags/bag1` contains 47 messages on `/number` (`example_interfaces/msg/Int64`) over approximately 46 seconds. Inspect or replay it with:

```bash
ros2 bag info bags/bag1
ros2 bag play bags/bag1
```

The bag plays independently; it is not started by the application launch files.

## Tests

Run the package tests after building:

```bash
colcon test
colcon test-result --verbose
```

The Python packages include standard ROS 2 lint tests for copyright headers, formatting, and docstrings.
