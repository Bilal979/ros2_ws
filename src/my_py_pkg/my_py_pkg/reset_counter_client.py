import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import ResetCounter

class ResetCounterClientNode(Node):
    def __init__(self):
        super().__init__("reset_counter_client")
        self._reset_counter_client = self.create_client(ResetCounter, "reset_counter")
        self.get_logger().info("reset_counter_clinet node started")


    def call_reset_counter(self, value):
        while not self._reset_counter_client.wait_for_service(1.0):
            self.get_logger.warn("Waiting for service")

        request = ResetCounter.Request()
        request.reset_value = value

        future = self._reset_counter_client.call_async(request)
        future.add_done_callback(self.callback_reset_counter_response)



    def callback_reset_counter_response(self, future):
        response = future.result()
        self.get_logger().info(f"Success flag: {response.success}")
        self.get_logger().info(f"Logger info: {response.message}")

    



def main(args=None):
    rclpy.init(args=args)
    node = ResetCounterClientNode()
    node.call_reset_counter(5)
    rclpy.spin(node)
    rclpy.shutdown()
        
