#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from my_robot_interfaces.srv import ResetCounter

class NumberCounterNode(Node):
    def __init__(self):
        super().__init__('number_counter')
        self._counter = 0
        self._number_subscriber = self.create_subscription(Int64, 'number', self.callback_number, 10)
        self._reset_counter_service = self.create_service(ResetCounter, 'reset_counter', self.callback_reset_counter)
        self.get_logger().info('Number counter has started')

    def callback_number(self, msg:Int64):
        self._counter += msg.data
        self.get_logger().info(f"Counter: {self._counter}")

    def callback_reset_counter(self, request:ResetCounter.Request, response:ResetCounter.Response):
        
        if request.reset_value < 0:
            response.success = False
            response.message = "Can not reset counter to a negative value"
        elif request.reset_value > self._counter:
            response.success = False
            response.message = "Reset value must be less than counter value"
        else:
            self._counter = request.reset_value
            self.get_logger().info(f"Reset counter to {self._counter}")
            response.success = True
            response.message = "Success"

        return response



def main(args=None):
    rclpy.init(args=args)
    node = NumberCounterNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()