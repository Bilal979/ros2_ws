#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
from my_robot_interfaces.srv import ActivateTurtle

class TurtleController(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self._current_position = "r"
        self._is_active = True
        self.cmd_vel_publisher_ = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.pose_subscription_ = self.create_subscription(Pose, "turtle1/pose", self.callback_pose, 10)
        self._set_pen_client = self.create_client(SetPen, "turtle1/set_pen")

        # activate turtle service
        self._activate_turtle_service = self.create_service(ActivateTurtle, 'activate_turtle', self.callback_activate_turtle)


    def callback_activate_turtle(self, request:ActivateTurtle.Request, response:ActivateTurtle.Response):

        if self._is_active == request.activate:
            response.success = False
            response.message = f"The turtle is already {'Active' if self._is_active else 'Deactive'}"
        else:
            self._is_active = request.activate
            response.success = True
            response.message = f"The turtle was {'Activated' if self._is_active else 'Deactivated'}"

        return response

        

    def callback_pose(self, msg:Pose):

        if not self._is_active:
            return
        
        twist_msg = Twist()
        twist_msg.linear.x = 1.0
        twist_msg.angular.z = 1.0
        position = 'l'

        if msg.x >= 5.5:
            twist_msg.linear.x = 2.0
            twist_msg.angular.z = 2.0
            position = 'r'

        self.cmd_vel_publisher_.publish(twist_msg)

        if self._current_position != position:
            self._current_position = position
            self.call_set_pen(position)


    def call_set_pen(self, value):
        while not self._set_pen_client.wait_for_service(1.0):
            self.get_logger().info("Waiting for set_pen service")

        request = SetPen.Request()

        request.r = 0
        request.g = 255
        request.width = 3

        if value == "r":
            request.r = 255
            request.g = 0

        future = self._set_pen_client.call_async(request)
        future.add_done_callback(self.callback_set_pen_response)


    def callback_set_pen_response(self, future):
        response = future.result()
        self.get_logger().info(f"{response}")
        self.get_logger().info("Turtle pen path updated")
        





def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()