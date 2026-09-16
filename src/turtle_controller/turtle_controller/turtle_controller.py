#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class TurtleController(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.cmd_vel_publisher_ = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.pose_subscription_ = self.create_subscription(Pose, "turtle1/pose", self.callback_pose, 10)

    def callback_pose(self, msg:Pose):
        twist_msg = Twist()
        twist_msg.linear.x = 1.0
        twist_msg.angular.z = 1.0

        if msg.x >= 5.5:
            twist_msg.linear.x = 2.0
            twist_msg.angular.z = 2.0

        self.cmd_vel_publisher_.publish(twist_msg)




def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()