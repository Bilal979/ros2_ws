#!/usr/bin/env python3

import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from my_robot_interfaces.action import CountUntil
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup


class CountUnitlServerNode(Node):
    def __init__(self):
        super().__init__("count_until_server")
        self.count_until_server_ = ActionServer(self, CountUntil, "count_until", goal_callback=self.goal_callback,
                                                execute_callback=self.execute_callback, cancel_callback=self.cancel_callback,
                                                callback_group=ReentrantCallbackGroup())
        self.get_logger().info('count_until action server started...')


    def cancel_callback(self, goal_handle:ServerGoalHandle):
        self.get_logger().info('Received a cancel request')
        # Can use goal_handle to add check whteher to accept/Reject Cancel req
        return CancelResponse.ACCEPT
    
    
    def goal_callback(self, goal_request:CountUntil.Goal):
        self.get_logger().info('Received a Goal')

        if goal_request.target_number <= 0:
            self.get_logger().warn('Target number must be greater than 0')
            return GoalResponse.REJECT

        self.get_logger().info('Accepting the Goal')
        return GoalResponse.ACCEPT


    def execute_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("Starting the Goal Execution")

        # Extract data from the goal
        target_number = goal_handle.request.target_number
        delay = goal_handle.request.delay
        result = CountUntil.Result()
        feedback = CountUntil.Feedback()
        counter = 0

        self.get_logger().info("Executing the goal")
        # Do the processing/execution
        for i in range(target_number):

            # Check if the goal has been cancled
            if goal_handle.is_cancel_requested:
                self.get_logger().info('Canceling Goal')
                # set the final state of the goal and return result
                goal_handle.canceled()
                result.reached_number = counter
                return result
                    
            counter +=1

            feedback.current_number = counter
            goal_handle.publish_feedback(feedback)
            
            self.get_logger().info(f"the current counter value is {counter}")
            time.sleep(delay)


        # Set the final state of the goal (abort/success/cancel)
        goal_handle.succeed()

        # return the result to client
        result.reached_number = counter
        return result

        



def main(args=None):
    rclpy.init(args=args)
    node = CountUnitlServerNode()
    rclpy.spin(node, MultiThreadedExecutor())
    rclpy.shutdown()

if __name__=="__main__":
    main()