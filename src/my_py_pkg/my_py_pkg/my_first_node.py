#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class MyCustomNode(Node):
    def __init__(self):
        super().__init__("my_node_name")
        # self.get_logger().info('Hello World')
        self._counter = 0
        self._timer = self.create_timer(1.0, self.print_hello)

    def print_hello(self):
        self.get_logger().info("Hello" + str(self._counter))
        self._counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = MyCustomNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
