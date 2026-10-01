#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from rclpy.parameter import Parameter

class NumberPublisherNode(Node):
    def __init__(self):
        super().__init__('number_publisher')
        # self._number = 2

        # Declare Parameters
        self.declare_parameter('number', 3)
        self.declare_parameter('publish_period',1.0)

        # Get Parameter Values
        self.number_ = self.get_parameter('number').value
        self.publish_period_ = self.get_parameter('publish_period').value

        # Set parameter callback
        self.add_post_set_parameters_callback(self.parameter_callback)

        self._number_publisher = self.create_publisher(Int64, 'number', 10)
        self._number_timer = self.create_timer(self.publish_period_, self.publish_number)
        self.get_logger().info('Number publisher has started')

    
    def publish_number(self):
        msg = Int64()
        msg.data = self.number_
        self._number_publisher.publish(msg)


    def parameter_callback(self, params: list[Parameter]):
        for param in params:
            # can acess param name,value and type
            if param.name == 'number':
                self.number_ = param.value


    
        


def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

