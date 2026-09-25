import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from my_robot_interfaces.action import CountUntil

class CountUntilClientNode(Node):
    def __init__(self):
        super().__init__('count_until_client')
        self.count_until_client_ = ActionClient(self, CountUntil, 'count_until')


    def send_goal(self, target_number, delay):
        while not self.count_until_client_.wait_for_server(1.0):
            self.get_logger().info('Waiting for the count_until Action Server')

        goal = CountUntil.Goal()
        goal.target_number = target_number
        goal.delay = delay

        future = self.count_until_client_.send_goal_async(goal)
        future.add_done_callback(self.callback_goal_response)


    def callback_goal_response(self, future):
        goal_handle:ClientGoalHandle = future.result()

        if goal_handle.accepted:
            self.get_logger().info('Goal got Accpeted')
            goal_handle.get_result_async().add_done_callback(self.callback_goal_result)
        else:
            self.get_logger().info('Goal got Rejected')


    def callback_goal_result(self, future):
        response = future.result()
        status = response.status
        result = response.result

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Success')
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error('Aborted')
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn('Cancelled')

        self.get_logger().info(f'The goal result (reached_number): ${result.reached_number}')


def main(args=None):
    rclpy.init(args=args)
    node = CountUntilClientNode()
    
    node.send_goal(-1, 0.5)
    
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()




        
