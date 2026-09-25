import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from my_robot_interfaces.action import CountUntil

class CountUntilClientNode(Node):
    def __init__(self):
        super().__init__('count_until_client')
        self.goal_handle_:ClientGoalHandle | None = None
        self.count_until_client_ = ActionClient(self, CountUntil, 'count_until')


    def send_goal(self, target_number, delay):
        while not self.count_until_client_.wait_for_server(1.0):
            self.get_logger().info('Waiting for the count_until Action Server')

        goal = CountUntil.Goal()
        goal.target_number = target_number
        goal.delay = delay

        future = self.count_until_client_.send_goal_async(goal, feedback_callback=self.feedback_callback)
        future.add_done_callback(self.callback_goal_response)


    def feedback_callback(self, feedback_msg):
        number = feedback_msg.feedback.current_number

        # Test cancel Goal Request
        if number >= 2:
            self.cancel_goal()
        self.get_logger().info(f'(from feedback def)The current_number is {number}')


    def callback_goal_response(self, future):
        self.goal_handle_:ClientGoalHandle = future.result()

        if self.goal_handle_.accepted:
            self.get_logger().info('Goal got Accpeted')
            self.goal_handle_.get_result_async().add_done_callback(self.callback_goal_result)
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

        self.get_logger().info(f'The goal result (reached_number): {result.reached_number}')


    def cancel_goal(self):
        self.get_logger().info('Senidng a goal cancel request')
        self.goal_handle_.cancel_goal_async()



def main(args=None):
    rclpy.init(args=args)
    node = CountUntilClientNode()
    
    node.send_goal(6, 0.5)
    
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()




        
